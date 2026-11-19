package th.co.scb.ace.boundaryfixture.passing.recovery.casewf.internal;

import th.co.scb.ace.boundaryfixture.passing.common.api.CustomerLookup;

/** RWB-TE-001 fixture AC2: depends only on a published common interface. */
class SampleService {

	private final CustomerLookup lookups;

	SampleService(CustomerLookup lookups) {
		this.lookups = lookups;
	}

	String label(String code) {
		return lookups.label(code);
	}
}