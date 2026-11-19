package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.time.LocalDate;

/** The business date a parameter read is resolved against (SPEC-RWB-E1-042-023). */
public interface BusinessDateProvider {

	LocalDate today();
}