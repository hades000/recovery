package th.co.scb.ace.demo.recovery.casewf.workflow;

import java.util.UUID;

/** Workflow naming fixed by ADR-011 and BS-6.2. */
public final class WorkflowIds {

	public static final String NAMESPACE = "rwb-recovery";
	public static final String QUEUE_CASE = "rwb-case";
	public static final String QUEUE_INTEGRATION = "rwb-integration";
	public static final String QUEUE_PLATFORM = "rwb-platform";

	/** Search attributes: Keyword, never personal data. */
	public static final String SA_CASE_ID = "CaseId";
	public static final String SA_STAGE = "Stage";
	public static final String SA_PRODUCT_GROUP = "ProductGroup";
	public static final String SA_QUEUE_CODE = "QueueCode";

	private WorkflowIds() {
	}

	/** One workflow per case: {@code case-{caseId}}. */
	public static String caseWorkflowId(UUID caseId) {
		return "case-" + caseId;
	}
}
