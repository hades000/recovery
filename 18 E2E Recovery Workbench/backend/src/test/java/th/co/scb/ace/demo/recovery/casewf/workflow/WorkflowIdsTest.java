package th.co.scb.ace.demo.recovery.casewf.workflow;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import org.junit.jupiter.api.Test;

/**
 * RWB-TE-001 SPEC-024: workflow names, queues, search attributes and the case workflow ID format
 * stay as ADR-011 and BS-6.2 fix them.
 */
class WorkflowIdsTest {

	@Test
	void namesFollowTheAgreedConventions() {
		assertThat(WorkflowIds.NAMESPACE).isEqualTo("rwb-recovery");
		assertThat(WorkflowIds.QUEUE_CASE).isEqualTo("rwb-case");
		assertThat(WorkflowIds.QUEUE_INTEGRATION).isEqualTo("rwb-integration");
		assertThat(WorkflowIds.QUEUE_PLATFORM).isEqualTo("rwb-platform");
		assertThat(WorkflowIds.SA_CASE_ID).isEqualTo("CaseId");
		assertThat(WorkflowIds.SA_STAGE).isEqualTo("Stage");
		assertThat(WorkflowIds.SA_PRODUCT_GROUP).isEqualTo("ProductGroup");
		assertThat(WorkflowIds.SA_QUEUE_CODE).isEqualTo("QueueCode");
	}

	@Test
	void caseWorkflowIdIsPrefixedWithCase() {
		UUID caseId = UUID.fromString("00000000-0000-0000-0000-000000000001");

		assertThat(WorkflowIds.caseWorkflowId(caseId)).isEqualTo("case-00000000-0000-0000-0000-000000000001");
	}
}
