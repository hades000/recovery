package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDate;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.FilterType;
import org.springframework.context.annotation.Import;
import org.springframework.dao.DataAccessResourceFailureException;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;

/**
 * TC-E1-042-24, TC-E1-042-31 and TC-E1-042-34 (SPEC-RWB-E1-042-011, -020, -025): the catalog endpoint
 * applies its four filters, renders PRODUCT rows without a value, refuses a role without the right
 * with the action text "read parameters", and turns a database failure into the status-only 503.
 */
@WebMvcTest(controllers = ParameterCatalogController.class,
		properties = { "rwb.p3.configservice=true", "rwb.environment=PROD" })
@Import(ParameterCatalogControllerTest.Security.class)
class ParameterCatalogControllerTest {

	@Autowired
	MockMvc mvc;

	@MockitoBean
	ParameterServiceImpl service;

	@MockitoBean
	CatalogSource catalog;

	@MockitoBean
	BusinessDateProvider businessDate;

	@TestConfiguration
	@EnableMethodSecurity
	@ComponentScan(basePackages = "th.co.scb.ace.demo.recovery.access.internal", useDefaultFilters = false,
			includeFilters = @ComponentScan.Filter(type = FilterType.REGEX,
					pattern = "th\\.co\\.scb\\.ace\\.demo\\.recovery\\.access\\.internal\\.(ProblemFactory|FixedMessageCatalog|InterimCapabilityCheck)"))
	static class Security {
	}

	@Test
	void filtersAndProductRowsWithoutValue() throws Exception {
		when(businessDate.today()).thenReturn(LocalDate.of(2026, 12, 1));
		when(catalog.all()).thenReturn(List.of(ParameterKeys.CASE_ENTRY_DPD, ParameterKeys.ENTRY_DPD,
				ParameterKeys.REFDATA_CACHE_TTL_SECONDS));
		when(service.inEnvironment(any(ParameterKey.class), anyString(), any(LocalDate.class)))
			.thenReturn((ParameterValue) new ParameterValue<>("case.entry.dpd", 30, 1, LocalDate.of(2026, 11, 2), "SIT"));
		when(service.inEnvironment(ParameterKeys.ENTRY_DPD, "SIT", LocalDate.of(2026, 12, 1))).thenReturn(null);
		when(service.inEnvironment(ParameterKeys.REFDATA_CACHE_TTL_SECONDS, "SIT", LocalDate.of(2026, 12, 1)))
			.thenReturn((ParameterValue) new ParameterValue<>("refdata.cache.ttl-seconds", 300, 0, null, "PROD"));

		MvcResult result = mvc.perform(get("/api/recovery/v1/admin/parameters").param("key", "case.")
			.param("environment", "SIT")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-COE"))))
			.andExpect(status().isOk())
			.andReturn();

		assertThat(result.getResponse().getContentAsString()).contains("case.entry.dpd").doesNotContain("ENTRY_DPD");
	}

	@Test
	void productRowHasNoValue() throws Exception {
		when(businessDate.today()).thenReturn(LocalDate.of(2026, 12, 1));
		when(catalog.all()).thenReturn(List.of(ParameterKeys.ENTRY_DPD));
		when(service.inEnvironment(ParameterKeys.ENTRY_DPD, "PROD", LocalDate.of(2026, 12, 1))).thenReturn(null);

		mvc.perform(get("/api/recovery/v1/admin/parameters")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-COE"))))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].key").value("ENTRY_DPD"))
			.andExpect(jsonPath("$[0].valueInForce").doesNotExist())
			.andExpect(jsonPath("$[0].default").doesNotExist());
	}

	@Test
	void refusalCarriesTheActionText() throws Exception {
		mvc.perform(get("/api/recovery/v1/admin/parameters")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-PHONECOL"))))
			.andExpect(status().isForbidden())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-002"))
			.andExpect(jsonPath("$.detail").value("You cannot read parameters here. Your role does not include it."));
	}

	@Test
	void secretIsListedWithoutValue() throws Exception {
		when(businessDate.today()).thenReturn(LocalDate.of(2026, 12, 1));
		when(catalog.all()).thenReturn(List.of(ParameterKeys.ACE_DB_PASSWORD));
		when(service.inEnvironment(ParameterKeys.ACE_DB_PASSWORD, "PROD", LocalDate.of(2026, 12, 1))).thenReturn(null);

		mvc.perform(get("/api/recovery/v1/admin/parameters")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-COE"))))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].key").value("ace.db.password"))
			.andExpect(jsonPath("$[0].secret").value(true))
			.andExpect(jsonPath("$[0].valueInForce").doesNotExist())
			.andExpect(jsonPath("$[0].default").doesNotExist());
	}

	/** SEC-042-01 / Ponytail Nice 9: only a listed environment reaches the cache. */
	@Test
	void anUnlistedEnvironmentIsRefused() throws Exception {
		when(businessDate.today()).thenReturn(LocalDate.of(2026, 12, 1));
		when(catalog.all()).thenReturn(List.of(ParameterKeys.CASE_ENTRY_DPD));

		mvc.perform(get("/api/recovery/v1/admin/parameters").param("environment", "some-made-up-environment")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-COE"))))
			.andExpect(status().isUnprocessableEntity())
			.andExpect(jsonPath("$.messageCode").value("MSG-GEN-002"))
			.andExpect(jsonPath("$.field").value("environment"));

		org.mockito.Mockito.verify(service, org.mockito.Mockito.never())
			.inEnvironment(any(ParameterKey.class), anyString(), any(LocalDate.class));
	}

	@Test
	void databaseFailureIsAStatusOnly503() throws Exception {
		when(businessDate.today()).thenReturn(LocalDate.of(2026, 12, 1));
		when(catalog.all()).thenReturn(List.of(ParameterKeys.CASE_ENTRY_DPD));
		when(service.inEnvironment(any(ParameterKey.class), anyString(), any(LocalDate.class)))
			.thenThrow(new DataAccessResourceFailureException("synthetic driver message"));

		mvc.perform(get("/api/recovery/v1/admin/parameters")
			.with(user("synthetic").authorities(new SimpleGrantedAuthority("RW-COE"))))
			.andExpect(status().isServiceUnavailable())
			.andExpect(jsonPath("$.type").value("urn:rwb:problem:unavailable"))
			.andExpect(jsonPath("$.messageCode").doesNotExist())
			.andExpect(jsonPath("$.detail").doesNotExist());
	}
}
