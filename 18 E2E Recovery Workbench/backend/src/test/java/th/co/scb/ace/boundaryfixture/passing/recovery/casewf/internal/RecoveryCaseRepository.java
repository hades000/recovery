package th.co.scb.ace.boundaryfixture.passing.recovery.casewf.internal;

import org.springframework.data.repository.Repository;

/** RWB-TE-001 fixture: repository of the same module. */
public interface RecoveryCaseRepository extends Repository<RecoveryCaseEntity, Long> {

	RecoveryCaseEntity save(RecoveryCaseEntity entity);
}