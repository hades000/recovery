package th.co.scb.ace.boundaryfixture.bnd2.recovery.casewf.internal;

import th.co.scb.ace.boundaryfixture.bnd2.common.api.CustomerLookup;

/** RWB-TE-001 fixture: a dependency on the published common package passes BND-2. */
class SampleLookupUser {

	private CustomerLookup lookups;
}