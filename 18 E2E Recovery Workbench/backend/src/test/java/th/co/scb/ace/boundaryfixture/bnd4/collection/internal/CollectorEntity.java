package th.co.scb.ace.boundaryfixture.bnd4.collection.internal;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

/** RWB-TE-001 fixture AC4: entity of the external collection root. */
@Entity
public class CollectorEntity {

	@Id
	private Long id;

	public Long id() {
		return id;
	}
}