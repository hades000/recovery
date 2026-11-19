package th.co.scb.ace.demo.recovery.casewf.config.api;

/** A secret parameter is never served (SPEC-RWB-E1-042-010). Holds the key only, never a value. */
public class SecretNotServedException extends RuntimeException {

	public SecretNotServedException(String key) {
		super(key);
	}
}