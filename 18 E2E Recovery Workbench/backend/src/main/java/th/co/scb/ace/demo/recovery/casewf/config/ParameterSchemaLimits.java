package th.co.scb.ace.demo.recovery.casewf.config;

/**
 * The schema limits this story checks in code, named instead of written as bare literals
 * (SPEC-RWB-E1-042-004, §12.11): the rollback reason is {@code varchar(400)} and the content hash is
 * {@code char(64)} in Physical Schema v6. Both are recorded in the magic-number baseline with the
 * reason "schema limit".
 */
final class ParameterSchemaLimits {

	/** {@code parameter_value.rollback_reason varchar(400)}. */
	static final int ROLLBACK_REASON_MAX = 400;

	/** {@code parameter_value.param_value varchar(400)}. */
	static final int PARAM_VALUE_MAX = 400;

	private ParameterSchemaLimits() {
	}
}