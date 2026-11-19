package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

/** JPA access to {@code parameter_value} (SPEC-RWB-E1-042-002, -007, -013..-015). */
interface ParameterValueRepository extends JpaRepository<ParameterValueEntity, UUID> {

	/** The APPROVED versions of a key and environment, oldest first. */
	@Query("""
			select v from ParameterValueEntity v
			where v.paramKey = :key and v.environment = :environment and v.status = 'APPROVED'
			order by v.validFrom""")
	List<ParameterValueEntity> approved(@Param("key") String key, @Param("environment") String environment);

	/** The highest version number over every status for (key, environment, GLOBAL). */
	@Query("""
			select coalesce(max(v.versionNo), 0) from ParameterValueEntity v
			where v.paramKey = :key and v.environment = :environment and v.productGroup is null""")
	int maxVersionNo(@Param("key") String key, @Param("environment") String environment);

	/** Every row of one load, locked for the approval or rollback transaction. */
	@Lock(LockModeType.PESSIMISTIC_WRITE)
	@Query("select v from ParameterValueEntity v where v.loadId = :loadId order by v.paramKey, v.environment")
	List<ParameterValueEntity> lockByLoadId(@Param("loadId") UUID loadId);

	@Query("select v from ParameterValueEntity v where v.loadId = :loadId order by v.paramKey, v.environment")
	List<ParameterValueEntity> findByLoadId(@Param("loadId") UUID loadId);

	/** An APPROVED row of (key, environment) whose valid_from is on or after the date. */
	@Query("""
			select count(v) from ParameterValueEntity v
			where v.paramKey = :key and v.environment = :environment and v.status = 'APPROVED'
			  and v.productGroup is null and v.validFrom >= :validFrom""")
	long countApprovedFrom(@Param("key") String key, @Param("environment") String environment,
			@Param("validFrom") LocalDate validFrom);

	/** The APPROVED rows of the given keys, every environment, for the validity recomputation. */
	@Query("""
			select v from ParameterValueEntity v
			where v.paramKey in :keys and v.status = 'APPROVED'
			order by v.validFrom""")
	List<ParameterValueEntity> findApproved(@Param("keys") List<String> keys);

	/** An APPROVED row of (key, environment) strictly earlier than the date. */
	@Query("""
			select count(v) from ParameterValueEntity v
			where v.paramKey = :key and v.environment = :environment and v.status = 'APPROVED'
			  and v.productGroup is null and v.validFrom < :validFrom""")
	long countApprovedBefore(@Param("key") String key, @Param("environment") String environment,
			@Param("validFrom") LocalDate validFrom);

	/**
	 * The advisory-lock keys of the distinct (key, environment) pairs of one load, in ascending order,
	 * read without loading or locking its rows. They are the values the lock is taken on, so sorting
	 * them gives one global lock order even when two pairs share a hash (REVIEW-001 CG-R001-02).
	 */
	@Query(value = """
			select distinct hashtext('parameter_value|' || param_key || '|' || environment) as lock_key
			from {h-schema}parameter_value where load_id = :loadId order by lock_key""", nativeQuery = true)
	List<Integer> keyEnvironmentLocksOf(@Param("loadId") UUID loadId);

	/**
	 * The content lock: a transaction-scoped advisory lock on {@code hashtext} of the key. It serialises
	 * two loads of the same content and date, so the second one finds the first as a repeat. The
	 * argument is bound, never formatted into the SQL.
	 */
	@Query(value = "select pg_advisory_xact_lock(hashtext(:key))", nativeQuery = true)
	void advisoryLock(@Param("key") String key);

	/**
	 * The (key, environment) lock: a transaction-scoped advisory lock on a key from
	 * {@link #keyEnvironmentLocksOf}. It serialises approvals and rollbacks of the same (key, environment)
	 * (REVIEW-001 H1). Callers take the keys in the ascending order that query returns, so every
	 * transaction takes them in one global order (CG-R001-02).
	 */
	@Query(value = "select pg_advisory_xact_lock(:key)", nativeQuery = true)
	void advisoryLock(@Param("key") int key);

	/**
	 * A load identified by (validFrom, content hash) for the identical-repeat case. A ROLLED_BACK load
	 * is not a repeat: SPEC-013 and the load check 11 allow a repeat for a VALIDATED or APPROVED load
	 * only, so the same CSV can be loaded again after a rollback (review Must 1).
	 */
	@Query("""
			select v from ParameterValueEntity v
			where v.validFrom = :validFrom and v.contentHash = :contentHash
			  and v.status in ('VALIDATED', 'APPROVED')
			order by v.paramKey, v.environment""")
	List<ParameterValueEntity> findByContent(@Param("validFrom") LocalDate validFrom,
			@Param("contentHash") String contentHash);
}