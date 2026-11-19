package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.security.SecureRandom;
import java.util.Base64;

import io.temporal.client.WorkflowClient;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.worker.WorkerFactory;
import org.junit.jupiter.api.Test;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ConfigurableApplicationContext;

import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 SPEC-024: {@code TemporalConfig} builds the client, codec and worker beans only when
 * {@code rwb.p3.temporal} is on, starts the workers on the ready event and requires the codec key.
 */
class TemporalConfigTest {

	@Test
	void flagOnCreatesTheClientCodecAndWorkerBeans() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(TemporalConfig.class)
			.withPropertyValues("rwb.p3.temporal=true", "rwb.temporal.target=127.0.0.1:7233",
					"rwb.temporal.codec-key=" + codecKey())
			.run(context -> {
				assertThat(context).hasNotFailed();
				assertThat(context).hasSingleBean(WorkflowServiceStubs.class);
				assertThat(context).hasSingleBean(PdpaPayloadCodec.class);
				assertThat(context).hasSingleBean(WorkflowClient.class);
				assertThat(context).hasSingleBean(WorkerFactory.class);
			});
	}

	@Test
	void flagOffCreatesNoTemporalBeans() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(TemporalConfig.class)
			.withPropertyValues("rwb.p3.temporal=false")
			.run(context -> {
				assertThat(context).hasNotFailed();
				assertThat(context).doesNotHaveBean(WorkflowServiceStubs.class);
				assertThat(context).doesNotHaveBean(WorkerFactory.class);
			});
	}

	@Test
	void startWorkersStartsTheFactory() {
		WorkerFactory factory = mock(WorkerFactory.class);
		ConfigurableApplicationContext context = mock(ConfigurableApplicationContext.class);
		when(context.getBean(WorkerFactory.class)).thenReturn(factory);
		ApplicationReadyEvent event = mock(ApplicationReadyEvent.class);
		when(event.getApplicationContext()).thenReturn(context);

		new TemporalConfig().startWorkers(event);

		verify(factory).start();
	}

	@Test
	void smokeActivityAnswersWithTheProbeAndTheHost() {
		PlatformSmokeWorkflow.SmokeResult result = new TemporalConfig.SmokeActivities().answer("probe-1");

		assertThat(result.probeId()).isEqualTo("probe-1");
		assertThat(result.answeredBy()).isNotBlank();
		assertThat(result.answeredAt()).isNotBlank();
	}

	@Test
	void hostNameIsNeverBlank() {
		assertThat(TemporalConfig.hostName()).isNotBlank();
	}

	@Test
	void blankCodecKeyFailsTheContext() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(TemporalConfig.class)
			.withPropertyValues("rwb.p3.temporal=true", "rwb.temporal.codec-key=")
			.run(context -> {
				assertThat(context).hasFailed();
				assertThat(context.getStartupFailure())
					.hasStackTraceContaining("rwb.temporal.codec-key is required");
			});
	}

	private static String codecKey() {
		byte[] key = new byte[32];
		new SecureRandom().nextBytes(key);
		return Base64.getEncoder().encodeToString(key);
	}
}
