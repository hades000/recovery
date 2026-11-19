package recovery.casewf.caselist;

import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;

/** Fixture for TC-E1-042-03 (a): an ad-hoc key that is not in the catalog. Not compiled. */
public class OtherReads {

	ParameterKey<Integer> adHoc() {
		return ParameterKey.of("allocation.retry.limit", Integer.class);
	}
}