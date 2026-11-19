package th.co.scb.ace.demo.recovery.access.internal;

import java.util.Collection;
import java.util.List;
import java.util.Map;

import org.springframework.context.annotation.Bean;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.http.HttpMethod;
import org.springframework.security.authorization.AuthorizationDecision;
import org.springframework.security.authorization.AuthorizationManager;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.security.oauth2.core.OAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2TokenValidatorResult;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtValidators;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.intercept.RequestAuthorizationContext;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import th.co.scb.ace.demo.recovery.access.api.ApiError;

/**
 * Entra ID bearer tokens (BS-4.1). Locally the issuer is the mock OIDC server; in SIT/UAT/PROD it is
 * the bank tenant. App roles in the {@code roles} claim become authorities with no prefix, so a
 * method check reads {@code hasAuthority('RW-PLATADM')}.
 *
 * <p>API Specification v4: E401 (MSG-P4-001) when there is no valid token <em>or</em> the person
 * holds no Workbench role; E403 (MSG-P4-002) when a role lacks the right. Every endpoint also
 * carries a method check naming its capability area (BS-3.2).
 */
@Configuration(proxyBeanMethods = false)
@EnableMethodSecurity
@EnableConfigurationProperties(RecoverySecurityProperties.class)
class SecurityConfig {

	static final String WORKBENCH_ROLE_PREFIX = "RW-";

	static final AuthorizationManager<RequestAuthorizationContext> HOLDS_WORKBENCH_ROLE =
			(auth, ctx) -> new AuthorizationDecision(holdsWorkbenchRole(auth.get()));

	static boolean holdsWorkbenchRole(Object principal) {
		return principal instanceof Authentication a && a.isAuthenticated()
				&& a.getAuthorities().stream().anyMatch(g -> g.getAuthority().startsWith(WORKBENCH_ROLE_PREFIX));
	}

	@Bean
	SecurityFilterChain recoverySecurity(HttpSecurity http, RecoverySecurityProperties properties, ProblemFactory problems)
			throws Exception {
		http
			.csrf(csrf -> csrf.disable()) // stateless bearer-token API, no cookies
			.cors(cors -> cors.configurationSource(corsSource(properties.corsOrigins())))
			.sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
			.authorizeHttpRequests(auth -> auth
				.requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
				.requestMatchers("/actuator/health/**", "/actuator/info").permitAll()
				.requestMatchers("/actuator/**").hasAuthority("RW-PLATADM")
				.requestMatchers("/api/recovery/**").access(HOLDS_WORKBENCH_ROLE)
				.anyRequest().denyAll())
			.exceptionHandling(e -> e
				.authenticationEntryPoint((req, res, ex) -> problems.write(res, ApiError.NO_ROLE, Map.of()))
				.accessDeniedHandler((req, res, ex) -> problems.write(res,
						holdsWorkbenchRole(req.getUserPrincipal()) ? ApiError.NOT_PERMITTED : ApiError.NO_ROLE,
						Map.of("action", "do this"))))
			.oauth2ResourceServer(o -> o
				.authenticationEntryPoint((req, res, ex) -> problems.write(res, ApiError.NO_ROLE, Map.of()))
				.jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter(properties))));
		return http.build();
	}

	@Bean
	JwtDecoder jwtDecoder(RecoverySecurityProperties properties) {
		RecoverySecurityProperties security = properties;
		NimbusJwtDecoder decoder = NimbusJwtDecoder.withJwkSetUri(security.jwkSetUri()).build();
		OAuth2TokenValidator<Jwt> audience = jwt -> jwt.getAudience() != null && jwt.getAudience().contains(security.audience())
				? OAuth2TokenValidatorResult.success()
				: OAuth2TokenValidatorResult.failure(new OAuth2Error("invalid_token", "audience not accepted", null));
		decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
				JwtValidators.createDefaultWithIssuer(security.issuer()), audience));
		return decoder;
	}

	private static JwtAuthenticationConverter jwtAuthenticationConverter(RecoverySecurityProperties properties) {
		String rolesClaim = properties.rolesClaim();
		Converter<Jwt, Collection<GrantedAuthority>> roles = jwt -> {
			List<String> values = jwt.getClaimAsStringList(rolesClaim);
			return values == null ? List.of()
					: values.stream().<GrantedAuthority>map(SimpleGrantedAuthority::new).toList();
		};
		JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
		converter.setJwtGrantedAuthoritiesConverter(roles);
		converter.setPrincipalClaimName("sub");
		return converter;
	}

	private static CorsConfigurationSource corsSource(List<String> origins) {
		CorsConfiguration cors = new CorsConfiguration();
		cors.setAllowedOrigins(origins == null ? List.of() : origins);
		cors.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
		cors.setAllowedHeaders(List.of("Authorization", "Content-Type", "Idempotency-Key", "X-Correlation-Id"));
		cors.setExposedHeaders(List.of("X-Correlation-Id"));
		UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
		source.registerCorsConfiguration("/api/**", cors);
		return source;
	}
}
