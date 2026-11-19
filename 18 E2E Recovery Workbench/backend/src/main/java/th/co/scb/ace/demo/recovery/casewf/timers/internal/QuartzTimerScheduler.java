package th.co.scb.ace.demo.recovery.casewf.timers.internal;

import java.time.Instant;
import java.util.Date;
import java.util.UUID;

import org.quartz.Job;
import org.quartz.JobBuilder;
import org.quartz.JobDataMap;
import org.quartz.JobDetail;
import org.quartz.JobExecutionContext;
import org.quartz.JobKey;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;
import org.quartz.Trigger;
import org.quartz.TriggerBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.casewf.timers.TimerScheduler;

/**
 * Epic 1-2 implementation of {@link TimerScheduler} on Quartz (BS-5.1, BS-5.2). The timer row in
 * {@code recovery.timer} stays the record; Quartz only fires it.
 *
 * <p>Locally Quartz uses its in-memory store. In ACE it uses the ACE JDBC job store.
 */
@Component
class QuartzTimerScheduler implements TimerScheduler {

	static final String GROUP = "rwb-timer";

	private final Scheduler scheduler;

	QuartzTimerScheduler(Scheduler scheduler) {
		this.scheduler = scheduler;
	}

	@Override
	public void schedule(UUID timerId, UUID caseId, String timerCode, Instant dueAt) {
		JobKey key = JobKey.jobKey(timerId.toString(), GROUP);
		JobDataMap data = new JobDataMap();
		data.put("timerId", timerId.toString());
		data.put("caseId", caseId.toString());
		data.put("timerCode", timerCode);
		data.put("dueAt", dueAt.toString());
		JobDetail job = JobBuilder.newJob(TimerDueJob.class).withIdentity(key).usingJobData(data).build();
		Trigger trigger = TriggerBuilder.newTrigger().withIdentity(timerId.toString(), GROUP)
				.startAt(Date.from(dueAt)).build();
		try {
			scheduler.scheduleJob(job, java.util.Set.of(trigger), true);
		}
		catch (SchedulerException ex) {
			throw new IllegalStateException("Timer could not be scheduled: " + timerId, ex);
		}
	}

	@Override
	public boolean cancel(UUID timerId) {
		try {
			return scheduler.deleteJob(JobKey.jobKey(timerId.toString(), GROUP));
		}
		catch (SchedulerException ex) {
			throw new IllegalStateException("Timer could not be cancelled: " + timerId, ex);
		}
	}

	/** Publishes {@link TimerDue}. Spring's Quartz integration autowires the publisher. */
	public static class TimerDueJob implements Job {

		private ApplicationEventPublisher events;

		@Autowired
		public void setEvents(ApplicationEventPublisher events) {
			this.events = events;
		}

		@Override
		public void execute(JobExecutionContext context) {
			JobDataMap data = context.getMergedJobDataMap();
			events.publishEvent(new TimerDue(UUID.fromString(data.getString("timerId")),
					UUID.fromString(data.getString("caseId")), data.getString("timerCode"),
					Instant.parse(data.getString("dueAt"))));
		}
	}
}
