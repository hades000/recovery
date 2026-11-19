package th.co.scb.ace.boundaryfixture.bnd4.legacy;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

/** RWB-TE-001 fixture AC4: entity outside every module and external root. */
@Entity
public class ArchivedLoanEntity {

	@Id
	private Long id;

	public Long id() {
		return id;
	}
}