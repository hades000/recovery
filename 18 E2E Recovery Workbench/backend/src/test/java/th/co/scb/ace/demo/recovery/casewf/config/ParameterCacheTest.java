package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Duration;
import java.time.LocalDate;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.ObjectProvider;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.CatalogEntry;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;

/**
 * TC-E1-042-11 and TC-E1-042-28 (SPEC-RWB-E1-042-009, -018): the cache holds the approved versions,
 * resolves the business date on every read, expires after its TTL, and rebuilds on the approval
 * event. The TTL read cannot recurse: while its own entry is rebuilt the generated default is used.
 */
class ParameterCacheTest {

	private static final LocalDate TODAY = LocalDate.of(2026, 12, 1);

	private ParameterValueRepository values;

	private BusinessDateProvider businessDate;

	private ParameterCache cache;

	@BeforeEach
	void setUp() {
		values = mock(ParameterValueRepository.class);
		businessDate = mock(BusinessDateProvider.class);
		when(businessDate.today()).thenReturn(TODAY);
		cache = new ParameterCache(values, provider(service(60)), businessDate);
	}

	@Test
	void aVersionStartsOnItsValidFromWithNoRestart() {
		when(values.approved("case.entry.dpd", "PROD")).thenReturn(List.of(
				row("case.entry.dpd", "PROD", "90", LocalDate.of(2026, 11, 2), null),
				row("case.entry.dpd", "PROD", "91", LocalDate.of(2026, 12, 10), null)));

		List<ParameterValueEntity> versions = cache.approved("case.entry.dpd", "PROD");

		// One cached list; the read path picks the version by date, so the future row starts on its day.
		assertThat(versions).hasSize(2);
		assertThat(versions.get(1).validFrom).isEqualTo(LocalDate.of(2026, 12, 10));
		verify(values, times(1)).approved("case.entry.dpd", "PROD");
	}

	@Test
	void anEntryExpiresAfterItsTtl() {
		when(values.approved("case.entry.dpd", "PROD")).thenReturn(List.of());
		ParameterCache expiring = new ParameterCache(values, provider(service(60)), businessDate) {
			@Override
			Duration ttl() {
				return Duration.ZERO;
			}
		};

		expiring.approved("case.entry.dpd", "PROD");
		expiring.approved("case.entry.dpd", "PROD");

		verify(values, times(2)).approved("case.entry.dpd", "PROD");
	}

	@Test
	void aRebuildAfterTheEventReReadsTheRows() {
		when(values.approved("case.entry.dpd", "PROD")).thenReturn(List.of());
		cache.approved("case.entry.dpd", "PROD");

		cache.invalidate("case.entry.dpd", "PROD");
		cache.approved("case.entry.dpd", "PROD");

		verify(values, times(2)).approved("case.entry.dpd", "PROD");
	}

	/** REVIEW-001 M9: the service reads back through the same cache, so only the guard stops the loop. */
	@Test
	void theTtlReadDoesNotRecurse() {
		AtomicReference<ParameterCache> self = new AtomicReference<>();
		ParameterCache guarded = new ParameterCache(values, provider(new RebuildingService(self)), businessDate);
		self.set(guarded);

		assertThat(guarded.ttl()).isEqualTo(Duration.ofSeconds(120));
		verify(values).approved(ParameterKeys.CONFIG_CACHE_TTL_SECONDS.name(), "PROD");
	}

	@Test
	void theGeneratedDefaultCoversAMissingTtlValue() {
		ParameterCache fallback = new ParameterCache(values, provider(new FailingService()), businessDate);

		assertThat(fallback.ttl()).isEqualTo(Duration.ofSeconds(Long.parseLong(
				ParameterKeys.CONFIG_CACHE_TTL_SECONDS.defaultValue())));
	}

	@Test
	void theTtlComesFromTheCachedValueWhenOneIsInForce() {
		assertThat(cache.ttl()).isEqualTo(Duration.ofSeconds(60));
	}

	@Test
	void invalidateAllClearsEveryEntry() {
		when(values.approved("case.entry.dpd", "PROD")).thenReturn(List.of());
		cache.approved("case.entry.dpd", "PROD");

		cache.invalidateAll();
		cache.approved("case.entry.dpd", "PROD");

		verify(values, times(2)).approved("case.entry.dpd", "PROD");
	}

	/** SEC-042-01: an entry that has expired is removed, so the singleton map cannot grow unbounded. */
	@Test
	void anExpiredEntryIsEvicted() {
		when(values.approved(anyString(), anyString())).thenReturn(List.of());
		ParameterCache expiring = new ParameterCache(values, provider(service(60)), businessDate) {
			@Override
			Duration ttl() {
				return Duration.ZERO;
			}
		};

		expiring.approved("case.entry.dpd", "PROD");
		expiring.approved("rules.testcases.min", "PROD");

		assertThat(expiring.entryCount()).as("only the live pair is cached").isEqualTo(1);
	}

	private static ParameterService service(int ttlSeconds) {
		return new StubService(ttlSeconds);
	}

	/**
	 * Answers the TTL key after reading it through the cache under test, as ParameterServiceImpl does,
	 * so the cache rebuilds its own entry and its re-entrancy guard is exercised.
	 */
	private static final class RebuildingService extends StubService {

		private final AtomicReference<ParameterCache> cache;

		private RebuildingService(AtomicReference<ParameterCache> cache) {
			super(120);
			this.cache = cache;
		}

		@Override
		public <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate) {
			cache.get().approved(key.name(), "PROD");
			return super.get(key, businessDate);
		}
	}

	private static final class FailingService extends StubService {

		private FailingService() {
			super(0);
		}

		@Override
		public <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate) {
			throw new ParameterNotInForceException(key.name());
		}
	}

	private static class StubService implements ParameterService {

		private final int ttlSeconds;

		private StubService(int ttlSeconds) {
			this.ttlSeconds = ttlSeconds;
		}

		@Override
		public <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate) {
			return new ParameterValue<>(key.name(), key.type().cast(Integer.valueOf(ttlSeconds)), 1, businessDate,
					"PROD");
		}

		@Override
		public <T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate) {
			return get(key, businessDate);
		}

		@Override
		public CatalogEntry entry(String key) {
			throw new UnsupportedOperationException();
		}
	}

	@SuppressWarnings("unchecked")
	private static ObjectProvider<ParameterService> provider(ParameterService service) {
		ObjectProvider<ParameterService> provider = mock(ObjectProvider.class);
		when(provider.getObject()).thenReturn(service);
		return provider;
	}

	static ParameterValueEntity row(String key, String environment, String value, LocalDate validFrom,
			String productGroup) {
		ParameterValueEntity row = new ParameterValueEntity();
		row.paramKey = key;
		row.environment = environment;
		row.paramValue = value;
		row.versionNo = 1;
		row.validFrom = validFrom;
		row.productGroup = productGroup;
		row.status = "APPROVED";
		return row;
	}
}
