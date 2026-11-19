package th.co.scb.ace.boundaryfixture.passing.recovery.casewf.internal;

/** RWB-TE-001 fixture: uses its own module's entity and repository. */
class CaseLoader {

	private final RecoveryCaseRepository repository;

	CaseLoader(RecoveryCaseRepository repository) {
		this.repository = repository;
	}

	RecoveryCaseEntity save(RecoveryCaseEntity entity) {
		return repository.save(entity);
	}
}