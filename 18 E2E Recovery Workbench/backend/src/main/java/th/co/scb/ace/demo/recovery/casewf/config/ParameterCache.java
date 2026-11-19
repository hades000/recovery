package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;

/**
 * Per-instance cache of the APPROVED versions of each (key, environment) pair (SPEC-RWB-E1-042-009,
 * -018). The business date is resolved on every read, so a version starts on its {@code valid_from}
 * with no restart and no rebuild; an entry expires after {@code config.cache.ttl-seconds}. While that
 * key's own entry is being rebuilt the generated default is used, so the TTL read cannot recurse
 * (PA-E1-042-03). The cache never holds VALIDATED or ROLLED_BACK rows and never a secret.
 */
@Component
class ParameterCache {

	/** One cached list and the instant it expires. */
	record Entry(List<ParameterValueEntity> versions, Instant expiresAt) {
	}

	private final ParameterValueRepository values;

	private final ObjectProvider<ParameterService> service;

	private final BusinessDateProvider businessDate;

	private final Map<String, Entry> entries = new ConcurrentHashMap<>();

	private final ThreadLocal<Boolean> resolvingTtl = ThreadLocal.withInitial(() -> false);

	ParameterCache(ParameterValueRepository values, ObjectProvider<ParameterService> service,
			BusinessDateProvider businessDate) {
		this.values = values;
		this.service = service;
		this.businessDate = businessDate;
	}

	List<ParameterValueEntity> approved(String key, String environment) {
		String cacheKey = key + "|" + environment;
		Instant now = Instant.now();
		Entry entry = entries.get(cacheKey);
		if (entry != null && entry.expiresAt().isAfter(now)) {
			return entry.versions();
		}
		List<ParameterValueEntity> versions = List.copyOf(values.approved(key, environment));
		// SEC-042-01: an expired pair is removed, so the singleton map cannot grow without bound.
		entries.entrySet().removeIf(cached -> !cached.getValue().expiresAt().isAfter(now));
		entries.put(cacheKey, new Entry(versions, now.plus(ttl())));
		return versions;
	}

	void invalidate(String key, String environment) {
		entries.remove(key + "|" + environment);
	}

	void invalidateAll() {
		entries.clear();
	}

	/** The number of cached pairs; a test asserts that an expired pair is evicted (SEC-042-01). */
	int entryCount() {
		return entries.size();
	}

	Duration ttl() {
		if (Boolean.TRUE.equals(resolvingTtl.get())) {
			return defaultTtl();
		}
		resolvingTtl.set(true);
		try {
			ParameterValue<Integer> value = service.getObject()
				.get(ParameterKeys.CONFIG_CACHE_TTL_SECONDS, businessDate.today());
			return Duration.ofSeconds(value.value().longValue());
		}
		catch (RuntimeException ex) {
			return defaultTtl();
		}
		finally {
			resolvingTtl.set(false);
		}
	}

	private static Duration defaultTtl() {
		return Duration.ofSeconds(Long.parseLong(ParameterKeys.CONFIG_CACHE_TTL_SECONDS.defaultValue()));
	}
}
