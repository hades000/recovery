package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowClientOptions;
import io.temporal.client.WorkflowOptions;
import io.temporal.common.converter.CodecDataConverter;
import io.temporal.common.converter.DefaultDataConverter;
import io.temporal.testing.TestEnvironmentOptions;
import io.temporal.testing.TestWorkflowEnvironment;
import io.temporal.testing.WorkflowReplayer;
import io.temporal.worker.Worker;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;

/** Worker start, activity retry, codec round trip and deterministic replay (testing-standards §3). */
class PlatformSmokeWorkflowTest {

	private TestWorkflowEnvironment env;
	private WorkflowClient client;
	private final AtomicInteger attempts = new AtomicInteger();

	private final PdpaPayloadCodec codec = new PdpaPayloadCodec(PdpaPayloadCodecTest.newKey(), "test");

	private TestWorkflowEnvironment newEnvironment() {
		return TestWorkflowEnvironment.newInstance(TestEnvironmentOptions.newBuilder()
				.setWorkflowClientOptions(WorkflowClientOptions.newBuilder()
						.setNamespace(WorkflowIds.NAMESPACE)
						.setDataConverter(new CodecDataConverter(DefaultDataConverter.newDefaultInstance(), List.of(codec)))
						.build())
				.build());
	}

	@BeforeEach
	void setUp() {
		env = newEnvironment();
		Worker worker = env.newWorker(WorkflowIds.QUEUE_PLATFORM);
		worker.registerWorkflowImplementationTypes(PlatformSmokeWorkflow.Impl.class);
		worker.registerActivitiesImplementations((PlatformSmokeWorkflow.Activities) probeId -> {
			if (attempts.incrementAndGet() == 1) {
				throw new IllegalStateException("first attempt fails");
			}
			return new PlatformSmokeWorkflow.SmokeResult(probeId, "test-host", "2026-11-17T00:00:00Z");
		});
		env.start();
		client = env.getWorkflowClient();
	}

	@AfterEach
	void tearDown() {
		env.close();
	}

	@Test
	void activityRetriesAndWorkflowAnswers() throws Exception {
		PlatformSmokeWorkflow workflow = client.newWorkflowStub(PlatformSmokeWorkflow.class,
				WorkflowOptions.newBuilder().setWorkflowId("platform-smoke-test").setTaskQueue(WorkflowIds.QUEUE_PLATFORM).build());

		PlatformSmokeWorkflow.SmokeResult result = workflow.run("probe-1");

		assertThat(result.probeId()).isEqualTo("probe-1");
		assertThat(result.answeredBy()).isEqualTo("test-host");
		assertThat(attempts).hasValue(2);

		var history = client.fetchHistory("platform-smoke-test");
		// Replay with the codec-aware environment: history holds only encrypted payloads.
		try (TestWorkflowEnvironment replay = newEnvironment()) {
			WorkflowReplayer.replayWorkflowExecution(history, replay, PlatformSmokeWorkflow.Impl.class);
		}
	}
}
