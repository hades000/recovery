package th.co.scb.ace.demo.recovery.access.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.options;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpHeaders;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 SPEC-024: the resource-server configuration keeps the 401/403 problem bodies, the
 * roles-claim mapping, the CORS origins and the open health path.
 */
@WebMvcTest(controllers = SecurityConfigTest.ProbeController.class, properties = {
		"rwb.security.issuer=http://localhost:8090/entra",
		"rwb.security.jwk-set-uri=http://localhost:8090/entra/jwks",
		"rwb.security.audience=api://rwb-recovery", "rwb.security.roles-claim=roles",
		"rwb.security.cors-origins=http://localhost:5173", "rwb.p3.temporal=false" })
@Import({ SecurityConfigTest.ProbeController.class, SecurityConfig.class, ProblemFactory.class,
		ApiExceptionHandler.class })
class SecurityConfigTest {

	@Autowired
	private MockMvc mvc;

	@MockitoBean
	private JwtDecoder jwtDecoder;

	@Test
	void bindsSecurityFromApplicationYaml() {
		ApplicationYamlEnvironment.runner().withUserConfiguration(PropertiesRegistration.class).run(context -> {
			assertThat(context).hasNotFailed();
			RecoverySecurityProperties properties = context.getBean(RecoverySecurityProperties.class);
			assertThat(properties.issuer()).isEqualTo("http://localhost:8090/entra");
			assertThat(properties.jwkSetUri()).isEqualTo("http://localhost:8090/entra/jwks");
			assertThat(properties.audience()).isEqualTo("api://rwb-recovery");
			assertThat(properties.rolesClaim()).isEqualTo("roles");
			assertThat(properties.corsOrigins()).containsExactly("http://localhost:5173");
		});
	}

	@Test
	void noTokenIs401WithMsgP4001() throws Exception {
		mvc.perform(get("/api/recovery/v1/test/probe"))
			.andExpect(status().isUnauthorized())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-001"));
	}

	@Test
	void tokenWithoutAWorkbenchRoleIs401WithMsgP4001() throws Exception {
		mvc.perform(get("/api/recovery/v1/test/probe")
			.with(jwt().authorities(new SimpleGrantedAuthority("SCOPE_read"))))
			.andExpect(status().isUnauthorized())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-001"));
	}

	@Test
	void workbenchRoleWithoutTheRightIs403WithMsgP4002() throws Exception {
		mvc.perform(get("/api/recovery/v1/test/probe")
			.with(jwt().authorities(new SimpleGrantedAuthority("RW-TEST"))))
			.andExpect(status().isForbidden())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-002"));
	}

	@Test
	void platformAdminReachesTheProbe() throws Exception {
		mvc.perform(get("/api/recovery/v1/test/probe")
			.with(jwt().authorities(new SimpleGrantedAuthority("RW-PLATADM"))))
			.andExpect(status().isOk());
	}

	@Test
	void rolesClaimBecomesAuthorities() throws Exception {
		when(jwtDecoder.decode("token")).thenReturn(jwtWithRoles(List.of("RW-PLATADM")));

		mvc.perform(get("/api/recovery/v1/test/probe").header(HttpHeaders.AUTHORIZATION, "Bearer token"))
			.andExpect(status().isOk());
	}

	@Test
	void missingRolesClaimGivesNoAuthority() throws Exception {
		when(jwtDecoder.decode("token")).thenReturn(jwtWithRoles(null));

		mvc.perform(get("/api/recovery/v1/test/probe").header(HttpHeaders.AUTHORIZATION, "Bearer token"))
			.andExpect(status().isUnauthorized())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-001"));
	}

	@Test
	void configuredOriginIsAllowedAndAnotherIsRefused() throws Exception {
		mvc.perform(options("/api/recovery/v1/test/probe")
			.header(HttpHeaders.ORIGIN, "http://localhost:5173")
			.header(HttpHeaders.ACCESS_CONTROL_REQUEST_METHOD, "GET"))
			.andExpect(status().isOk())
			.andExpect(header().string(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, "http://localhost:5173"));

		mvc.perform(options("/api/recovery/v1/test/probe")
			.header(HttpHeaders.ORIGIN, "http://other.example")
			.header(HttpHeaders.ACCESS_CONTROL_REQUEST_METHOD, "GET"))
			.andExpect(status().isForbidden());
	}

	@Test
	void healthIsOpenSoTheSliceAnswersNotAuthorised() throws Exception {
		mvc.perform(get("/actuator/health")).andExpect(status().isNotFound());
	}

	@Test
	void holdsWorkbenchRoleIsFalseWithoutAnAuthenticationOrWithNoWorkbenchAuthority() {
		Authentication unauthenticated = org.mockito.Mockito.mock(Authentication.class);
		org.mockito.Mockito.when(unauthenticated.isAuthenticated()).thenReturn(false);

		assertThat(SecurityConfig.holdsWorkbenchRole("anonymous")).isFalse();
		assertThat(SecurityConfig.holdsWorkbenchRole(unauthenticated)).isFalse();
		assertThat(SecurityConfig.holdsWorkbenchRole(new org.springframework.security.authentication.AnonymousAuthenticationToken(
				"key", "anonymous", List.of(new SimpleGrantedAuthority("ROLE_ANONYMOUS"))))).isFalse();
	}

	@Test
	void jwtDecoderIsBuiltFromThePropertiesWithoutANetworkCall() {
		JwtDecoder decoder = new SecurityConfig().jwtDecoder(new RecoverySecurityProperties(
				"http://localhost:8090/entra", "http://localhost:8090/entra/jwks", "api://rwb-recovery", "roles",
				List.of("http://localhost:5173")));

		assertThat(decoder).isInstanceOf(NimbusJwtDecoder.class);
	}

	private static Jwt jwtWithRoles(List<String> roles) {
		Jwt.Builder builder = Jwt.withTokenValue("token")
			.header("alg", "none")
			.subject("synthetic-user")
			.issuedAt(Instant.now())
			.expiresAt(Instant.now().plusSeconds(60));
		if (roles != null) {
			builder.claim("roles", roles);
		}
		return builder.build();
	}

	@Configuration(proxyBeanMethods = false)
	@EnableConfigurationProperties(RecoverySecurityProperties.class)
	static class PropertiesRegistration {
	}

	/** Probe inside {@code /api/recovery/**} so the URL rule passes and the method check decides. */
	@RestController
	static class ProbeController {

		@GetMapping("/api/recovery/v1/test/probe")
		@PreAuthorize("hasAuthority('RW-PLATADM')")
		String probe() {
			return "ok";
		}
	}
}
