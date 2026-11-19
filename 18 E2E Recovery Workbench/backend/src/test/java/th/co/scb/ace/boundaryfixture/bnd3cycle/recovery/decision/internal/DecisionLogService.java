package th.co.scb.ace.boundaryfixture.bnd3cycle.recovery.decision.internal;

import th.co.scb.ace.boundaryfixture.bnd3cycle.recovery.integration.api.CaseEvents;
import th.co.scb.ace.boundaryfixture.bnd3cycle.recovery.decision.writer.DecisionLogWriter;

/** RWB-TE-001 fixture AC3: decision depends on integration, which depends on decision. */
class DecisionLogService {

	private CaseEvents events;

	private DecisionLogWriter writer;
}