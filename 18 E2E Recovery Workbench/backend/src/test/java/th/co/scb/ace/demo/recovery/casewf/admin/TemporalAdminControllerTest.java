package th.co.scb.ace.demo.recovery.casewf.admin;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.time.Duration;
import java.util.List;

import io.grpc.Status;
import io.grpc.StatusRuntimeException;
import io.temporal.api.common.v1.WorkflowExecution;
import io.temporal.api.namespace.v1.NamespaceConfig;
import io.temporal.api.namespace.v1.NamespaceInfo;
import io.temporal.api.enums.v1.NamespaceState;
import io.temporal.api.taskqueue.v1.PollerInfo;
import io.temporal.api.workflowservice.v1.DescribeNamespaceRequest;
import io.temporal.api.workflowservice.v1.DescribeNamespaceResponse;
import io.temporal.api.workflowservice.v1.DescribeTaskQueueRequest;
import io.temporal.api.workflowservice.v1.DescribeTaskQueueResponse;
import io.temporal.client.WorkflowServiceException;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.testing.TestWorkflowEnvironment;
import io.temporal.worker.Worker;
import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;
import th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow;
import th.co.scb.ace.demo.recovery.casewf.workflow.internal.TemporalProperties;

/**
 * RWB-TE-001 SPEC-024: {@code TemporalAdminController} reports namespace and queue health, maps an
 * unavailable Temporal frontend to 503 MSG-P3-036 and starts the smoke workflow once per day.
 */
class TemporalAdminControllerTest {

	private static final TemporalProperties PROPERTIES = new TemporalProperties("localhost:7233", "rwb-recovery",
			null, null, Duration.ofSeconds(5));

	@Test
	void healthReportsNamespaceStateRetentionAndQueues() {
		WorkflowServiceStubs stubs = mock(WorkflowServiceStubs.class);
		io.temporal.api.workflowservice.v1.WorkflowServiceGrpc.WorkflowServiceBlockingStub blocking = mock(io.temporal.api.workflowservice.v1.WorkflowServiceGrpc.WorkflowServiceBlockingStub.class);
		when(stubs.blockingStub()).thenReturn(blocking);
		when(blocking.describeNamespace(any(DescribeNamespaceRequest.class))).thenReturn(DescribeNamespaceResponse
			.newBuilder()
			.setNamespaceInfo(NamespaceInfo.newBuilder().setName("rwb-recovery")
				.setState(NamespaceState.NAMESPACE_STATE_REGISTERED))
			.setConfig(NamespaceConfig.newBuilder()
				.setWorkflowExecutionRetentionTtl(com.google.protobuf.Duration.newBuilder().setSeconds(2_592_000)))
			.build());
		when(blocking.describeTaskQueue(any(DescribeTaskQueueRequest.class)))
			.thenReturn(DescribeTaskQueueResponse.newBuilder().addPollers(PollerInfo.getDefaultInstance()).addPollers(PollerInfo.getDefaultInstance()).addPollers(PollerInfo.getDefaultInstance()).build());

		TemporalAdminController.TemporalHealth health = new TemporalAdminController(stubs, null, PROPERTIES).health();

		assertThat(health.target()).isEqualTo("localhost:7233");
		assertThat(health.namespace()).isEqualTo("rwb-recovery");
		assertThat(health.state()).isEqualTo("NAMESPACE_STATE_REGISTERED");
		assertThat(health.retentionDays()).isEqualTo(30);
		assertThat(health.taskQueues()).extracting(TemporalAdminController.QueueHealth::name)
			.containsExactly(WorkflowIds.QUEUE_CASE, WorkflowIds.QUEUE_INTEGRATION, WorkflowIds.QUEUE_PLATFORM);
		assertThat(health.taskQueues()).extracting(TemporalAdminController.QueueHealth::workflowPollers)
			.containsExactly(3, 3, 3);
	}

	@Test
	void unavailableTemporalFrontendIs503WithMsgP3036() {
		TemporalAdminController controller = controllerFailingWith(new StatusRuntimeException(Status.UNAVAILABLE));

		assertThatThrownBy(controller::health).isInstanceOfSatisfying(ApiProblemException.class,
				exception -> assertThat(exception.error()).isEqualTo(ApiError.WORKFLOW_UNAVAILABLE));
	}

	@Test
	void deadlineExceededIs503WithMsgP3036() {
		TemporalAdminController controller = controllerFailingWith(
				new StatusRuntimeException(Status.DEADLINE_EXCEEDED));

		assertThatThrownBy(controller::health).isInstanceOfSatisfying(ApiProblemException.class,
				exception -> assertThat(exception.error()).isEqualTo(ApiError.WORKFLOW_UNAVAILABLE));
	}

	@Test
	void otherStatusIsRethrown() {
		StatusRuntimeException failure = new StatusRuntimeException(Status.INTERNAL);
		TemporalAdminController controller = controllerFailingWith(failure);

		assertThatThrownBy(controller::health).isSameAs(failure);
	}

	@Test
	void workflowServiceExceptionWithUnavailableCauseIs503() {
		WorkflowServiceException failure = new WorkflowServiceException(WorkflowExecution.newBuilder()
			.setWorkflowId("platform-smoke-29990101")
			.build(), "PlatformSmokeWorkflow", new StatusRuntimeException(Status.UNAVAILABLE));
		TemporalAdminController controller = controllerFailingWith(failure);

		assertThatThrownBy(controller::health).isInstanceOfSatisfying(ApiProblemException.class,
				exception -> assertThat(exception.error()).isEqualTo(ApiError.WORKFLOW_UNAVAILABLE));
	}

	@Test
	void workflowServiceExceptionWithOtherCauseIsRethrown() {
		WorkflowServiceException failure = new WorkflowServiceException(WorkflowExecution.newBuilder()
			.setWorkflowId("platform-smoke-29990101")
			.build(), "PlatformSmokeWorkflow", new IllegalStateException("synthetic"));
		TemporalAdminController controller = controllerFailingWith(failure);

		assertThatThrownBy(controller::health).isSameAs(failure);
	}

	@Test
	void smokeStartsTheDailyPlatformSmokeWorkflow() {
		TestWorkflowEnvironment environment = TestWorkflowEnvironment.newInstance();
		try {
			Worker worker = environment.newWorker(WorkflowIds.QUEUE_PLATFORM);
			worker.registerWorkflowImplementationTypes(PlatformSmokeWorkflow.Impl.class);
			worker.registerActivitiesImplementations(new PlatformSmokeWorkflow.Activities() {
				@Override
				public PlatformSmokeWorkflow.SmokeResult answer(String probeId) {
					return new PlatformSmokeWorkflow.SmokeResult(probeId, "test-host", "2999-01-01T00:00:00Z");
				}
			});
			environment.start();
			TemporalAdminController controller = new TemporalAdminController(null,
					environment.getWorkflowClient(), PROPERTIES);

			TemporalAdminController.SmokeStarted first = controller.smoke();
			TemporalAdminController.SmokeStarted second = controller.smoke();

			assertThat(first.workflowId()).matches("platform-smoke-\\d{8}");
			assertThat(first.workflowType()).isEqualTo("PlatformSmokeWorkflow");
			assertThat(second.workflowId()).isEqualTo(first.workflowId());
		}
		finally {
			environment.close();
		}
	}

	private static TemporalAdminController controllerFailingWith(RuntimeException failure) {
		WorkflowServiceStubs stubs = mock(WorkflowServiceStubs.class);
		io.temporal.api.workflowservice.v1.WorkflowServiceGrpc.WorkflowServiceBlockingStub blocking = mock(io.temporal.api.workflowservice.v1.WorkflowServiceGrpc.WorkflowServiceBlockingStub.class);
		when(stubs.blockingStub()).thenReturn(blocking);
		when(blocking.describeNamespace(any(DescribeNamespaceRequest.class))).thenThrow(failure);
		return new TemporalAdminController(stubs, null, PROPERTIES);
	}
}
