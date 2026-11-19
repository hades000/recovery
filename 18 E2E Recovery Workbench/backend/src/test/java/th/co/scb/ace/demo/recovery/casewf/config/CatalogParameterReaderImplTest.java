package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.LocalDate;
import java.util.NoSuchElementException;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;
import th.co.scb.ace.demo.recovery.casewf.config.api.SecretNotServedException;

/**
 * TC-E1-042-46 (SPEC-RWB-E1-042-026, -023; D-RUN-19): the P4 reader delegates to
 * {@link ParameterService}, throws only JDK exception types, and its messages hold the key only.
 */
class CatalogParameterReaderImplTest {

	private static final LocalDate DATE = LocalDate.of(2026, 12, 1);

	private ParameterService service;

	private BusinessDateProvider businessDate;

	private CatalogParameterReaderImpl reader;

	@BeforeEach
	void setUp() {
		service = mock(ParameterService.class);
		businessDate = mock(BusinessDateProvider.class);
		when(businessDate.today()).thenReturn(DATE);
		reader = new CatalogParameterReaderImpl(service, businessDate);
	}

	@Test
	void delegatesAndThrowsJdkTypesOnly() {
		when(service.get(ParameterKeys.CASE_ENTRY_DPD, DATE))
			.thenReturn(new ParameterValue<>("case.entry.dpd", 90, 1, LocalDate.of(2026, 11, 2), "PROD"));

		CatalogParameterReaderImpl.Value<Integer> value = reader.get("case.entry.dpd", Integer.class, DATE);

		assertThat(value.key()).isEqualTo("case.entry.dpd");
		assertThat(value.value()).isEqualTo(90);
		assertThat(value.versionNo()).isEqualTo(1);
		assertThat(value.environment()).isEqualTo("PROD");
	}

	@Test
	void twoArgumentGetUsesTheProviderDate() {
		when(service.get(ParameterKeys.CASE_ENTRY_DPD, DATE))
			.thenReturn(new ParameterValue<>("case.entry.dpd", 90, 0, null, "PROD"));

		assertThat(reader.get("case.entry.dpd", Integer.class).value()).isEqualTo(90);
		verify(businessDate).today();
	}

	@Test
	void anUnknownKeyOrAWrongTypeIsIllegalArgument() {
		assertThatThrownBy(() -> reader.get("not.a.key", Integer.class, DATE))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessage("not.a.key");
		assertThatThrownBy(() -> reader.get("case.entry.dpd", String.class, DATE))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessage("case.entry.dpd");
	}

	@Test
	void aProductKeyIsIllegalArgument() {
		assertThatThrownBy(() -> reader.get("ENTRY_DPD", Integer.class, DATE))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessage("ENTRY_DPD");
	}

	@Test
	void aSecretKeyIsIllegalState() {
		when(service.get(ParameterKeys.ACE_DB_PASSWORD, DATE))
			.thenThrow(new SecretNotServedException("ace.db.password"));

		assertThatThrownBy(() -> reader.get("ace.db.password", String.class, DATE))
			.isInstanceOf(IllegalStateException.class)
			.hasMessage("ace.db.password");
	}

	@Test
	void nothingInForceAndNoDefaultIsNoSuchElement() {
		when(service.get(ParameterKeys.TEMPORAL_TASKQUEUE_PLATFORM, DATE))
			.thenThrow(new ParameterNotInForceException("temporal.taskqueue.platform"));

		assertThatThrownBy(() -> reader.get("temporal.taskqueue.platform", String.class, DATE))
			.isInstanceOf(NoSuchElementException.class)
			.hasMessage("temporal.taskqueue.platform");
	}

	@Test
	void aDefaultIsServedWithVersionZero() {
		when(service.get(ParameterKeys.CASE_ENTRY_DPD, DATE))
			.thenReturn(new ParameterValue<>("case.entry.dpd", 90, 0, null, "PROD"));

		CatalogParameterReaderImpl.Value<Integer> value = reader.get("case.entry.dpd", Integer.class, DATE);

		assertThat(value.versionNo()).isZero();
		assertThat(value.validFrom()).isNull();
	}

	@Test
	void noMessageHoldsAValue() {
		when(service.get(ParameterKeys.ACE_DB_PASSWORD, DATE))
			.thenThrow(new SecretNotServedException("ace.db.password"));

		assertThatThrownBy(() -> reader.get("ace.db.password", String.class, DATE))
			.hasMessage("ace.db.password")
			.satisfies(ex -> assertThat(ex.getMessage()).doesNotContain("="));
	}
}
