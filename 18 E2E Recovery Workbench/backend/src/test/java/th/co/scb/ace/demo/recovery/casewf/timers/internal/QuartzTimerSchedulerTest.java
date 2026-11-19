package th.co.scb.ace.demo.recovery.casewf.timers.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anySet;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Instant;
import java.util.UUID;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.quartz.JobDataMap;
import org.quartz.JobDetail;
import org.quartz.JobExecutionContext;
import org.quartz.JobKey;
import org.quartz.Scheduler;
import org.springframework.context.ApplicationEventPublisher;

import th.co.scb.ace.demo.recovery.casewf.timers.TimerScheduler.TimerDue;

class QuartzTimerSchedulerTest {

	private final Scheduler scheduler = mock(Scheduler.class);
	private final QuartzTimerScheduler timers = new QuartzTimerScheduler(scheduler);

	@Test
	void schedulesAReplaceableJobPerTimer() throws Exception {
		UUID timerId = UUID.randomUUID();
		UUID caseId = UUID.randomUUID();
		Instant due = Instant.parse("2027-01-15T02:00:00Z");

		timers.schedule(timerId, caseId, "T-SYNTHETIC", due);

		ArgumentCaptor<JobDetail> job = ArgumentCaptor.forClass(JobDetail.class);
		verify(scheduler).scheduleJob(job.capture(), anySet(), eq(true));
		assertThat(job.getValue().getKey()).isEqualTo(JobKey.jobKey(timerId.toString(), QuartzTimerScheduler.GROUP));
		assertThat(job.getValue().getJobDataMap().getString("caseId")).isEqualTo(caseId.toString());
	}

	@Test
	void cancelReportsWhetherATimerExisted() throws Exception {
		UUID timerId = UUID.randomUUID();
		when(scheduler.deleteJob(any())).thenReturn(true, false);
		assertThat(timers.cancel(timerId)).isTrue();
		assertThat(timers.cancel(timerId)).isFalse();
	}

	@Test
	void dueJobPublishesTimerDue() {
		ApplicationEventPublisher events = mock(ApplicationEventPublisher.class);
		QuartzTimerScheduler.TimerDueJob job = new QuartzTimerScheduler.TimerDueJob();
		job.setEvents(events);
		UUID timerId = UUID.randomUUID();
		UUID caseId = UUID.randomUUID();
		JobDataMap data = new JobDataMap();
		data.put("timerId", timerId.toString());
		data.put("caseId", caseId.toString());
		data.put("timerCode", "T-SYNTHETIC");
		data.put("dueAt", "2027-01-15T02:00:00Z");
		JobExecutionContext context = mock(JobExecutionContext.class);
		when(context.getMergedJobDataMap()).thenReturn(data);

		job.execute(context);

		verify(events).publishEvent(new TimerDue(timerId, caseId, "T-SYNTHETIC", Instant.parse("2027-01-15T02:00:00Z")));
	}
}
