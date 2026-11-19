package th.co.scb.ace.boundaryfixture.bnd3fail.recovery.integration.internal;

import th.co.scb.ace.boundaryfixture.bnd3fail.recovery.decision.internal.DecisionLogRepository;

/** RWB-TE-001 fixture AC3: uses another module's internal type, so verify() fails. */
class CaseSync {

	private DecisionLogRepository repository;
}