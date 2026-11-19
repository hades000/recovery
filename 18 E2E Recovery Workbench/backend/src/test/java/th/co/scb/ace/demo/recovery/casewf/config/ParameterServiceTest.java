package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.core.env.Environment;

import th.co.scb.ace.demo.recovery.casewf.config.api.CatalogEntry;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;
import th.co.scb.ace.demo.recovery.casewf.config.api.SecretNotServedException;

/**
 * TC-E1-042-01, -09, -11 and -26 (SPEC-RWB-E1-042-007, -008, -010, -024): the read service resolves
 * the value in force, falls back to the catalog default, refuses a secret and a PRODUCT key, serves
 * an ENV key from the property, converts every type, and returns the catalog-only view.
 */
class ParameterServiceTest {

	private static final LocalDate DATE = LocalDate.of(2026, 12, 1);

	private ParameterCache cache;

	private CatalogSource catalog;

	private Environment environment;

	private ParameterServiceImpl service;

	@BeforeEach
	void setUp() {
		cache = mock(ParameterCache.class);
		catalog = new CatalogSource();
		environment = mock(Environment.class);
		service = new ParameterServiceImpl(cache, catalog, environment, true, "PROD");
	}

	@Test
	void seededValueInForceReturnsValueVersionAndValidFrom() {
		when(cache.approved("case.entry.dpd", "PROD")).thenReturn(List.of(row("case.entry.dpd", "PROD", "95", 2,
				LocalDate.of(2026, 11, 2), null)));

		ParameterValue<Integer> value = service.get(ParameterKeys.CASE_ENTRY_DPD, DATE);

		assertThat(value.value()).isEqualTo(95);
		assertThat(value.versionNo()).isEqualTo(2);
		assertThat(value.validFrom()).isEqualTo(LocalDate.of(2026, 11, 2));
		assertThat(value.environment()).isEqualTo("PROD");
		assertThat(value.key()).isEqualTo("case.entry.dpd");
	}

	@Test
	void beforeTheFirstValidFromTheDefaultIsServed() {
		when(cache.approved("case.entry.dpd", "PROD")).thenReturn(List.of(row("case.entry.dpd", "PROD", "95", 2,
				LocalDate.of(2026, 12, 10), null)));

		ParameterValue<Integer> value = service.get(ParameterKeys.CASE_ENTRY_DPD, DATE);

		assertThat(value.value()).isEqualTo(90);
		assertThat(value.versionNo()).isZero();
		assertThat(value.validFrom()).isNull();
	}

	@Test
	void nothingInForceAndNoDefaultThrows() {
		when(environment.getProperty("rwb.temporal.target")).thenReturn(null);

		assertThatThrownBy(() -> service.get(ParameterKeys.TEMPORAL_TARGET, DATE))
			.isInstanceOf(ParameterNotInForceException.class)
			.hasMessage("temporal.target");
	}

	@Test
	void secretIsNeverServed() {
		assertThatThrownBy(() -> service.get(ParameterKeys.ACE_DB_PASSWORD, DATE))
			.isInstanceOf(SecretNotServedException.class)
			.hasMessage("ace.db.password");
	}

	@Test
	void productKeyThrowsParameterNotInForce() {
		assertThatThrownBy(() -> service.get(ParameterKeys.ENTRY_DPD, DATE))
			.isInstanceOf(ParameterNotInForceException.class)
			.hasMessage("ENTRY_DPD");
		assertThatThrownBy(() -> service.get(ParameterKeys.ENTRY_DPD, "MORTGAGE", DATE))
			.isInstanceOf(ParameterNotInForceException.class);
	}

	@Test
	void envKeyIsServedFromTheProperty() {
		when(environment.getProperty("rwb.drools.kiebase-cache-max")).thenReturn("35");

		ParameterValue<Integer> value = service.get(ParameterKeys.DROOLS_KIEBASE_CACHE_MAX, DATE);

		assertThat(value.value()).isEqualTo(35);
		assertThat(value.versionNo()).isZero();
		assertThat(value.validFrom()).isNull();
	}

	@Test
	void eachTypeConverts() {
		assertThat(convert(ParameterKeys.CASE_ENTRY_DPD, "90")).isEqualTo(90);
		assertThat(convert(ParameterKeys.RECON_CASELIST_TOLERANCE_PCT, "1.25")).isEqualTo(new BigDecimal("1.25"));
		assertThat(convert(ParameterKeys.SERVICELEVEL_REQUIRED_STATUSES, "NEW, ASSIGNED"))
			.isEqualTo(List.of("NEW", "ASSIGNED"));
		assertThat(convert(ParameterKeys.CASELIST_ALLOCATION_WAIT_UNTIL, "07:15")).isEqualTo(LocalTime.of(7, 15));
		assertThat(ParameterServiceImpl.typeName(ParameterKeys.CASE_ENTRY_DPD.type())).isEqualTo("INTEGER");
		assertThat(ParameterServiceImpl.typeName(ParameterKeys.SERVICELEVEL_REQUIRED_STATUSES.type()))
			.isEqualTo("CODE_LIST");
		assertThat(ParameterServiceImpl.typeName(ParameterKeys.RECON_CASELIST_TOLERANCE_PCT.type()))
			.isEqualTo("DECIMAL");
		assertThat(ParameterKey.of("fixture.boolean", Boolean.class).type()).isEqualTo(Boolean.class);
		assertThat(ParameterKey.of("fixture.date", LocalDate.class).type()).isEqualTo(LocalDate.class);
		assertThat(ParameterKey.of("fixture.duration", Duration.class).type()).isEqualTo(Duration.class);
		assertThat(ParameterKey.of("fixture.string", String.class).type()).isEqualTo(String.class);
	}

	@Test
	void entryReturnsTheCatalogViewWithNoValue() {
		CatalogEntry entry = service.entry("servicelevel.required-statuses");

		assertThat(entry.key()).isEqualTo("servicelevel.required-statuses");
		assertThat(entry.type()).isEqualTo("CODE_LIST");
		assertThat(entry.required()).isTrue();
		assertThat(entry.owner()).isEqualTo("RW-COE");
		assertThat(entry.environments()).containsExactly("DEV", "SIT", "UAT", "PROD");
		assertThat(entry.usedBy()).isEqualTo(List.of("recovery.casewf.refdata.product"));
	}

	@Test
	void productGroupOverloadResolvesTheProductRowFirstThenGlobal() {
		when(cache.approved("case.entry.dpd", "PROD")).thenReturn(List.of(
				row("case.entry.dpd", "PROD", "90", 1, LocalDate.of(2026, 11, 2), null),
				row("case.entry.dpd", "PROD", "45", 1, LocalDate.of(2026, 11, 2), "MORTGAGE")));

		assertThat(service.get(ParameterKeys.CASE_ENTRY_DPD, "MORTGAGE", DATE).value()).isEqualTo(45);
		assertThat(service.get(ParameterKeys.CASE_ENTRY_DPD, "HP", DATE).value()).isEqualTo(90);
	}

	@Test
	void eachEnvironmentResolvesItsOwnValue() {
		when(cache.approved("case.entry.dpd", "SIT")).thenReturn(List.of(
				row("case.entry.dpd", "SIT", "30", 1, LocalDate.of(2026, 11, 2), null)));
		when(cache.approved("case.entry.dpd", "PROD")).thenReturn(List.of(
				row("case.entry.dpd", "PROD", "300", 1, LocalDate.of(2026, 11, 2), null)));

		assertThat(service.inEnvironment(ParameterKeys.CASE_ENTRY_DPD, "SIT", DATE).value()).isEqualTo(30);
		assertThat(service.inEnvironment(ParameterKeys.CASE_ENTRY_DPD, "PROD", DATE).value()).isEqualTo(300);
	}

	@Test
	void withTheFlagOffOnlyDefaultsAndEnvValuesAreServed() {
		ParameterServiceImpl off = new ParameterServiceImpl(cache, catalog, environment, false, "PROD");

		assertThat(off.get(ParameterKeys.CASE_ENTRY_DPD, DATE).value()).isEqualTo(90);
		assertThat(off.get(ParameterKeys.CASE_ENTRY_DPD, DATE).versionNo()).isZero();
		assertThatThrownBy(() -> off.get(ParameterKeys.TEMPORAL_TARGET, DATE))
			.isInstanceOf(ParameterNotInForceException.class);
		org.mockito.Mockito.verifyNoInteractions(cache);
	}

	@Test
	void anUnknownEntryKeyIsRefused() {
		assertThatThrownBy(() -> service.entry("not.a.key")).isInstanceOf(IllegalArgumentException.class);
	}

	private static Object convert(ParameterKey<?> key, String text) {
		return ParameterValues.convert(cast(key), text);
	}

	@SuppressWarnings("unchecked")
	private static <T> ParameterKey<T> cast(ParameterKey<?> key) {
		return (ParameterKey<T>) key;
	}

	static ParameterValueEntity row(String key, String environment, String value, int versionNo, LocalDate validFrom,
			String productGroup) {
		ParameterValueEntity row = new ParameterValueEntity();
		row.paramKey = key;
		row.environment = environment;
		row.paramValue = value;
		row.versionNo = versionNo;
		row.validFrom = validFrom;
		row.validTo = null;
		row.productGroup = productGroup;
		row.status = "APPROVED";
		return row;
	}
}
