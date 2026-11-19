package th.co.scb.ace.boundaryfixture.passing.recovery.casewf.workflow.internal;

import th.co.scb.ace.boundaryfixture.passing.recovery.casewf.workflow.WorkflowPort;

/** RWB-TE-001 fixture: public type in an unlisted sub-package of a published package is allowed. */
public class WorkflowRunner implements WorkflowPort {

	@Override
	public void run(String probeId) {
	}
}