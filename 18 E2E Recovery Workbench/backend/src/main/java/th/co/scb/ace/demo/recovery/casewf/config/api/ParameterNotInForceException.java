package th.co.scb.ace.demo.recovery.casewf.config.api;

/** Nothing is in force for the key and it has no default (SPEC-RWB-E1-042-007). Holds the key only. */
public class ParameterNotInForceException extends RuntimeException {

	public ParameterNotInForceException(String key) {
		super(key);
	}
}