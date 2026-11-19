package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/**
 * The port the approval and the rollback call inside their own transaction, before commit
 * (SPEC-RWB-E1-042-019; REVIEW-001 M5). Implementations use {@code Propagation.MANDATORY} and throw on
 * failure, so a decision that cannot be recorded stops the approval or the rollback. The outcome
 * ({@code APPROVED} or {@code ROLLED_BACK}) says what was decided (REVIEW-001 CG-R001-01). Not published: the decision-log store is RWB-E1-008 and
 * RWB-E1-027.
 */
interface VersionDecisionRecorder {

	void recorded(String decisionCode, String outcome, String table, UUID loadId, List<String> keys,
			LocalDate validFrom, UUID approverUserId);
}