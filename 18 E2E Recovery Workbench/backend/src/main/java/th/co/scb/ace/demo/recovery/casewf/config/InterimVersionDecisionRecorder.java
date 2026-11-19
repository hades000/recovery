package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/**
 * Interim recorder (SPEC-RWB-E1-042-019, -027): one structured line with the load ID, the table, the
 * keys, the valid-from date, the decision code and the outcome. The approver's user ID is personal
 * data and is passed to the real decision log only, never logged here.
 */
@Component
class InterimVersionDecisionRecorder implements VersionDecisionRecorder {

	private static final Logger log = LoggerFactory.getLogger(InterimVersionDecisionRecorder.class);

	@Override
	@Transactional(propagation = Propagation.MANDATORY)
	public void recorded(String decisionCode, String outcome, String table, UUID loadId, List<String> keys,
			LocalDate validFrom, UUID approverUserId) {
		log.info("Parameter decision recorded decision={} outcome={} table={} loadId={} keys={} validFrom={}",
				decisionCode, outcome, table, loadId, String.join(",", keys), validFrom);
	}
}