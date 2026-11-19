package th.co.scb.ace.boundaryfixture.passing.recovery.casewf.internal;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

/** RWB-TE-001 fixture: entity used by a class of its own module. */
@Entity
public class RecoveryCaseEntity {

	@Id
	private Long id;

	public Long id() {
		return id;
	}
}