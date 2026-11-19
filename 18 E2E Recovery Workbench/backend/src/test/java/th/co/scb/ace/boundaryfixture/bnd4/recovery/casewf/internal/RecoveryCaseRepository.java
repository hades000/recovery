package th.co.scb.ace.boundaryfixture.bnd4.recovery.casewf.internal;

import org.springframework.data.repository.Repository;

/** RWB-TE-001 fixture AC4: repository of the casewf module. */
public interface RecoveryCaseRepository extends Repository<RecoveryCaseEntity, Long> {

	RecoveryCaseEntity save(RecoveryCaseEntity entity);
}