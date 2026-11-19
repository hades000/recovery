package th.co.scb.ace.demo.recovery.casewf.config;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.dao.DataAccessResourceFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.transaction.CannotCreateTransactionException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;

/**
 * {@code GET /api/recovery/v1/admin/parameters} (SPEC-RWB-E1-042-011, -020, -025): the catalog with
 * the value in force for the requested environment and the business date, filtered by key prefix,
 * kind and owner. The method check names the area and the operation. The flag switches the endpoint
 * off; a database that cannot be reached becomes the status-only 503 of E7, never a retry promise.
 */
@RestController
@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")
@RequestMapping("/api/recovery/v1/admin/parameters")
class ParameterCatalogController {

	private static final java.util.Set<String> ENVIRONMENTS = java.util.Set.of("DEV", "SIT", "UAT", "PROD");

	private final ParameterServiceImpl service;

	private final CatalogSource catalog;

	private final BusinessDateProvider businessDate;

	private final String runningEnvironment;

	ParameterCatalogController(ParameterServiceImpl service, CatalogSource catalog,
			@Value("${rwb.environment}") String runningEnvironment, BusinessDateProvider businessDate) {
		this.service = service;
		this.catalog = catalog;
		this.runningEnvironment = runningEnvironment;
		this.businessDate = businessDate;
	}

	@GetMapping
	@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")
	List<CatalogParameterView> list(@RequestParam(required = false) String key,
			@RequestParam(required = false) String kind, @RequestParam(required = false) String owner,
			@RequestParam(required = false) String environment) {
		String requested = environment == null || environment.isBlank() ? runningEnvironment : environment;
		requireAllowedEnvironment(requested);
		try {
			List<CatalogParameterView> views = new ArrayList<>();
			for (ParameterKey<?> definition : catalog.all()) {
				if (!matches(definition, key, kind, owner)) {
					continue;
				}
				views.add(view(definition, requested));
			}
			return views;
		}
		catch (DataAccessResourceFailureException | CannotCreateTransactionException ex) {
			throw new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, null, java.util.Map.of(), null, null, ex);
		}
	}

	private CatalogParameterView view(ParameterKey<?> definition, String environment) {
		ParameterValue<?> value = service.inEnvironment(definition, environment, businessDate.today());
		return new CatalogParameterView(definition.name(), definition.kind(),
				ParameterServiceImpl.typeName(definition.type()), emptyToNull(definition.unit()),
				emptyToNull(definition.min()), emptyToNull(definition.max()),
				definition.secret() ? null : definition.defaultValue(), definition.scope(), definition.required(),
				definition.ownerRole(), definition.environments(), definition.usedBy(), definition.secret(),
				value == null ? null : render(value.value()), value == null ? null : value.versionNo(),
				value == null ? null : value.validFrom());
	}

	/**
	 * A value outside the four environments is refused before any read, so an arbitrary string can
	 * never become a cache key (SEC-042-01). The API has no 422 for this operation yet; the delta is
	 * recorded for the OpenAPI owner.
	 */
	private static void requireAllowedEnvironment(String environment) {
		if (environment == null || environment.isBlank() || ENVIRONMENTS.contains(environment)) {
			return;
		}
		throw new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY, "MSG-GEN-002",
				java.util.Map.of("field", "environment", "min", "DEV", "max", "PROD"), "environment", null, null);
	}

	private static boolean matches(ParameterKey<?> definition, String key, String kind, String owner) {
		if (key != null && !key.isBlank() && !definition.name().startsWith(key)) {
			return false;
		}
		if (kind != null && !kind.isBlank() && !definition.kind().equals(kind.toUpperCase(Locale.ROOT))) {
			return false;
		}
		return owner == null || owner.isBlank() || definition.ownerRole().equals(owner);
	}

	private static String render(Object value) {
		if (value instanceof java.util.List<?> list) {
			return String.join(",", list.stream().map(String::valueOf).toList());
		}
		return String.valueOf(value);
	}

	private static String emptyToNull(String value) {
		return value == null || value.isEmpty() ? null : value;
	}
}
