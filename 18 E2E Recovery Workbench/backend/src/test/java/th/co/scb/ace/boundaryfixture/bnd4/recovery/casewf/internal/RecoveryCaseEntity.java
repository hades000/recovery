package th.co.scb.ace.boundaryfixture.bnd4.recovery.casewf.internal;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

/** RWB-TE-001 fixture AC4: entity of the casewf module. */
@Entity
public class RecoveryCaseEntity {

	@Id
	private Long id;

	public Long id() {
		return id;
	}
}