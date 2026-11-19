package th.co.scb.ace.demo.recovery.casewf.admin;

import java.time.Clock;
import java.time.Duration;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

import io.grpc.Status;
import io.grpc.StatusRuntimeException;
import io.temporal.api.enums.v1.TaskQueueType;
import io.temporal.api.taskqueue.v1.TaskQueue;
import io.temporal.api.workflowservice.v1.DescribeNamespaceRequest;
import io.temporal.api.workflowservice.v1.DescribeNamespaceResponse;
import io.temporal.api.workflowservice.v1.DescribeTaskQueueRequest;
import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowExecutionAlreadyStarted;
import io.temporal.client.WorkflowOptions;
import io.temporal.client.WorkflowServiceException;
import io.temporal.serviceclient.WorkflowServiceStubs;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow;
import th.co.scb.ace.demo.recovery.casewf.workflow.internal.TemporalProperties;
import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;

/**
 * Temporal operations, capability area Platform administration (module P3). Operational only: the
 * case API never exposes workflow internals. Not registered when {@code rwb.p3.temporal} is off, so
 * both paths return 404 (API Specification v4).
 */
@RestController
@RequestMapping("/api/recovery/v1/admin")
@ConditionalOnProperty(name = "rwb.p3.temporal", havingValue = "true")
class TemporalAdminController {

	private static final List<String> QUEUES = List.of(WorkflowIds.QUEUE_CASE, WorkflowIds.QUEUE_INTEGRATION,
			WorkflowIds.QUEUE_PLATFORM);
	private static final ZoneId BANK_ZONE = ZoneId.of("Asia/Bangkok");
	private static final DateTimeFormatter YYYYMMDD = DateTimeFormatter.BASIC_ISO_DATE;

	private final WorkflowServiceStubs stubs;
	private final WorkflowClient client;
	private final TemporalProperties properties;
	private final Clock clock;

	TemporalAdminController(WorkflowServiceStubs stubs, WorkflowClient client, TemporalProperties properties) {
		this.stubs = stubs;
		this.client = client;
		this.properties = properties;
		this.clock = Clock.system(BANK_ZONE);
	}

	/** Backend-context §3 and §7: namespace state, retention and pollers per task queue. */
	@GetMapping("/temporal/health")
	@PreAuthorize("hasAnyAuthority('RW-PLATADM', 'RW-AUDIT')") // Platform administration, right R
	TemporalHealth health() {
		return temporal(() -> {
			DescribeNamespaceResponse ns = stubs.blockingStub().describeNamespace(
					DescribeNamespaceRequest.newBuilder().setNamespace(properties.namespace()).build());
			List<QueueHealth> queues = QUEUES.stream().map(q -> new QueueHealth(q,
					stubs.blockingStub().describeTaskQueue(DescribeTaskQueueRequest.newBuilder()
							.setNamespace(properties.namespace())
							.setTaskQueue(TaskQueue.newBuilder().setName(q).build())
							.setTaskQueueType(TaskQueueType.TASK_QUEUE_TYPE_WORKFLOW)
							.build()).getPollersCount()))
					.toList();
			long retentionDays = Duration.ofSeconds(ns.getConfig().getWorkflowExecutionRetentionTtl().getSeconds()).toDays();
			return new TemporalHealth(properties.target(), ns.getNamespaceInfo().getName(),
					ns.getNamespaceInfo().getState().name(), retentionDays, queues);
		});
	}

	/**
	 * {@code POST /admin/workflows/smoke} (operationId postAdminWorkflowsSmoke). Starts
	 * {@code platform-smoke-{yyyymmdd}} on {@code rwb-platform} and returns 202. A running execution
	 * with that ID is returned as it is, not started twice.
	 */
	@PostMapping("/workflows/smoke")
	@ResponseStatus(HttpStatus.ACCEPTED)
	@PreAuthorize("hasAuthority('RW-PLATADM')") // Platform administration, right C
	SmokeStarted smoke() {
		String workflowId = "platform-smoke-" + LocalDate.now(clock).format(YYYYMMDD);
		PlatformSmokeWorkflow workflow = client.newWorkflowStub(PlatformSmokeWorkflow.class, WorkflowOptions.newBuilder()
				.setWorkflowId(workflowId)
				.setTaskQueue(WorkflowIds.QUEUE_PLATFORM)
				.setWorkflowExecutionTimeout(Duration.ofMinutes(1))
				.build());
		return temporal(() -> {
			try {
				WorkflowClient.start(workflow::run, workflowId);
			}
			catch (WorkflowExecutionAlreadyStarted running) {
				// Duplicate ID: hand back the running execution.
			}
			return new SmokeStarted(workflowId, "PlatformSmokeWorkflow");
		});
	}

	/** Temporal frontend unreachable: 503 MSG-P3-036. */
	private static <T> T temporal(Supplier<T> call) {
		try {
			return call.get();
		}
		catch (StatusRuntimeException ex) {
			if (isUnavailable(ex.getStatus())) {
				throw new ApiProblemException(ApiError.WORKFLOW_UNAVAILABLE, Map.of(), ex);
			}
			throw ex;
		}
		catch (WorkflowServiceException ex) {
			if (ex.getCause() instanceof StatusRuntimeException s && isUnavailable(s.getStatus())) {
				throw new ApiProblemException(ApiError.WORKFLOW_UNAVAILABLE, Map.of(), ex);
			}
			throw ex;
		}
	}

	private static boolean isUnavailable(Status status) {
		return status.getCode() == Status.Code.UNAVAILABLE || status.getCode() == Status.Code.DEADLINE_EXCEEDED;
	}

	record SmokeStarted(String workflowId, String workflowType) {
	}

	record TemporalHealth(String target, String namespace, String state, long retentionDays, List<QueueHealth> taskQueues) {
	}

	record QueueHealth(String name, int workflowPollers) {
	}
}
