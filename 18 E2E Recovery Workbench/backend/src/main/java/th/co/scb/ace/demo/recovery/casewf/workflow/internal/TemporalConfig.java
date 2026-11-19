package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.Instant;
import java.util.List;

import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowClientOptions;
import io.temporal.common.converter.CodecDataConverter;
import io.temporal.common.converter.DefaultDataConverter;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.serviceclient.WorkflowServiceStubsOptions;
import io.temporal.worker.Worker;
import io.temporal.worker.WorkerFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.event.EventListener;

import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;

/**
 * Temporal client and worker (ADR-011). Only built when {@code rwb.p3.temporal} is on; with the flag
 * off there is no connection, no worker and no Temporal admin endpoint.
 *
 * <p>The ADR names the Temporal Spring Boot starter; it does not support Spring Boot 4.1 yet, so the
 * SDK is wired here with the same settings. Swapping to the starter later changes only this class.
 * Locally the connection is plaintext; SIT/UAT/PROD use mTLS.
 */
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(name = "rwb.p3.temporal", havingValue = "true")
@EnableConfigurationProperties(TemporalProperties.class)
class TemporalConfig {

	private static final Logger log = LoggerFactory.getLogger(TemporalConfig.class);

	@Bean(destroyMethod = "shutdown")
	WorkflowServiceStubs workflowServiceStubs(TemporalProperties properties) {
		return WorkflowServiceStubs.newServiceStubs(WorkflowServiceStubsOptions.newBuilder()
				.setTarget(properties.target())
				.setRpcTimeout(properties.rpcTimeout())
				.build());
	}

	@Bean
	PdpaPayloadCodec pdpaPayloadCodec(TemporalProperties properties) {
		return new PdpaPayloadCodec(properties.codecKey(), properties.codecKeyId());
	}

	@Bean
	WorkflowClient workflowClient(WorkflowServiceStubs stubs, TemporalProperties properties, PdpaPayloadCodec codec) {
		return WorkflowClient.newInstance(stubs, WorkflowClientOptions.newBuilder()
				.setNamespace(properties.namespace())
				.setIdentity("ace-recovery@" + hostName())
				.setDataConverter(new CodecDataConverter(DefaultDataConverter.newDefaultInstance(), List.of(codec)))
				.build());
	}

	@Bean(destroyMethod = "shutdown")
	WorkerFactory workerFactory(WorkflowClient client) {
		WorkerFactory factory = WorkerFactory.newInstance(client);
		Worker platform = factory.newWorker(WorkflowIds.QUEUE_PLATFORM);
		platform.registerWorkflowImplementationTypes(PlatformSmokeWorkflow.Impl.class);
		platform.registerActivitiesImplementations(new SmokeActivities());
		// rwb-case and rwb-integration workers are registered by the Epic 3 case workflow stories.
		return factory;
	}

	@EventListener(ApplicationReadyEvent.class)
	void startWorkers(ApplicationReadyEvent event) {
		WorkerFactory factory = event.getApplicationContext().getBean(WorkerFactory.class);
		factory.start();
		log.info("Temporal workers started on task queue {}", WorkflowIds.QUEUE_PLATFORM);
	}

	/** Clock and host lookups are activity work, never workflow work (BS-6.1). */
	static final class SmokeActivities implements PlatformSmokeWorkflow.Activities {

		@Override
		public PlatformSmokeWorkflow.SmokeResult answer(String probeId) {
			return new PlatformSmokeWorkflow.SmokeResult(probeId, hostName(), Instant.now().toString());
		}
	}

	static String hostName() {
		try {
			return InetAddress.getLocalHost().getHostName();
		}
		catch (UnknownHostException ex) {
			return "unknown";
		}
	}
}
