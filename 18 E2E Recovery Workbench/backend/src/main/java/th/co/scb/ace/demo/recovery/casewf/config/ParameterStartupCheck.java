package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicReference;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Component;
import org.springframework.transaction.TransactionException;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;

/**
 * Readiness indicator {@code parameterCatalog} (SPEC-RWB-E1-042-016): for every required GLOBAL
 * non-secret key listed for the running environment, an approved row in force on the business date or
 * a generated default keeps the key UP; an ENV key is UP when its property resolves. A missing key
 * turns readiness DOWN with {@code MSG-P3-032} and its {@code {name, environment}} list, one WARN line
 * per key with the standard's English text, and the process keeps running (CLAR-012).
 *
 * <p>REVIEW-001 M6: a database that cannot be read is reported as {@code database: unavailable}, not as
 * every key missing, and the WARN lines are written only when the readiness state changes, not on
 * every probe.
 */
@Component("parameterCatalog")
class ParameterStartupCheck implements HealthIndicator {

	private static final Logger log = LoggerFactory.getLogger(ParameterStartupCheck.class);

	private static final String MESSAGE_CODE = "MSG-P3-032";

	private final CatalogSource catalog;

	private final ParameterServiceImpl service;

	private final BusinessDateProvider businessDate;

	private final org.springframework.core.env.Environment environment;

	private final boolean enabled;

	private final String runningEnvironment;

	/** The last state logged: UP, the database outage, or the missing keys. */
	private final AtomicReference<Object> logged = new AtomicReference<>();

	ParameterStartupCheck(CatalogSource catalog, ParameterServiceImpl service, BusinessDateProvider businessDate,
			org.springframework.core.env.Environment environment,
			@Value("${rwb.p3.configservice:false}") boolean enabled,
			@Value("${rwb.environment}") String runningEnvironment) {
		this.catalog = catalog;
		this.service = service;
		this.businessDate = businessDate;
		this.environment = environment;
		this.enabled = enabled;
		this.runningEnvironment = runningEnvironment;
	}

	@Override
	public Health health() {
		LocalDate today = businessDate.today();
		List<Map<String, String>> missing = new ArrayList<>();
		try {
			for (ParameterKey<?> key : catalog.all()) {
				if (!key.required() || !"GLOBAL".equals(key.scope()) || key.secret()
						|| !key.environments().contains(runningEnvironment)) {
					continue;
				}
				if (!up(key, today)) {
					Map<String, String> detail = new LinkedHashMap<>();
					detail.put("name", key.name());
					detail.put("environment", runningEnvironment);
					missing.add(detail);
				}
			}
		}
		catch (DataAccessException | TransactionException ex) {
			if (changed("database unavailable")) {
				log.warn("Parameter catalog readiness: the database is unavailable ({}).", ex.getClass().getSimpleName());
			}
			return Health.down().withDetail("database", "unavailable").build();
		}
		if (missing.isEmpty()) {
			changed("UP");
			return Health.up().build();
		}
		if (changed(List.copyOf(missing))) {
			for (Map<String, String> detail : missing) {
				log.warn("Parameter {} has no value for {}. The service did not start.", detail.get("name"),
						detail.get("environment"));
			}
		}
		return Health.down()
			.withDetail("messageCode", MESSAGE_CODE)
			.withDetail("missing", missing)
			.build();
	}

	private boolean up(ParameterKey<?> key, LocalDate today) {
		if ("ENV".equals(key.valueSource())) {
			String value = environment.getProperty(key.envProperty());
			return value != null && !value.isBlank();
		}
		if (!enabled && key.defaultValue() != null) {
			return true;
		}
		if (enabled) {
			try {
				ParameterValue<?> value = service.get(key, today);
				return value != null;
			}
			catch (DataAccessException | TransactionException ex) {
				throw ex;
			}
			catch (RuntimeException ex) {
				return false;
			}
		}
		return key.defaultValue() != null;
	}

	private boolean changed(Object state) {
		return !Objects.equals(logged.getAndSet(state), state);
	}
}
