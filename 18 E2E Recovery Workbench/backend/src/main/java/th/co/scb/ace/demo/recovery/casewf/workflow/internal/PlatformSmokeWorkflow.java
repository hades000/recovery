package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import java.time.Duration;

import io.temporal.activity.ActivityInterface;
import io.temporal.activity.ActivityOptions;
import io.temporal.common.RetryOptions;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

/**
 * Smoke workflow on task queue {@code rwb-platform} (ADR-011): proves the worker polls, an activity
 * runs and retries, and payloads round-trip through the codec. It carries no case data.
 */
@WorkflowInterface
public interface PlatformSmokeWorkflow {

	@WorkflowMethod
	SmokeResult run(String probeId);

	record SmokeResult(String probeId, String answeredBy, String answeredAt) {
	}

	@ActivityInterface
	interface Activities {

		SmokeResult answer(String probeId);
	}

	/** Deterministic: no clock, random or I/O here; those live in the activity (BS-6.1). */
	class Impl implements PlatformSmokeWorkflow {

		private final Activities activities = Workflow.newActivityStub(Activities.class,
				ActivityOptions.newBuilder()
						.setStartToCloseTimeout(Duration.ofSeconds(5))
						.setRetryOptions(RetryOptions.newBuilder().setMaximumAttempts(3).build())
						.build());

		@Override
		public SmokeResult run(String probeId) {
			return activities.answer(probeId);
		}
	}
}
