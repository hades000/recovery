package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.time.ZoneId;

import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;

/**
 * The business date until a platform provider arrives (SPEC-RWB-E1-042-023): today's date in
 * Asia/Bangkok, fixed in this class. It is not read from configuration.
 */
@Component
class InterimBusinessDateProvider implements BusinessDateProvider {

	private static final ZoneId ZONE = ZoneId.of("Asia/Bangkok");

	@Override
	public LocalDate today() {
		return LocalDate.now(ZONE);
	}
}