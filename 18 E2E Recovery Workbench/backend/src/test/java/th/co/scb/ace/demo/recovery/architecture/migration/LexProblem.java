package th.co.scb.ace.demo.recovery.architecture.migration;

/**
 * SPEC-RWB-E1-044-007: one unterminated opener still open at end of file. It feeds L-LEX, so a
 * stray opener can never hide the rest of the file from the lint.
 */
public record LexProblem(String kind, int line, int offset) {
}
