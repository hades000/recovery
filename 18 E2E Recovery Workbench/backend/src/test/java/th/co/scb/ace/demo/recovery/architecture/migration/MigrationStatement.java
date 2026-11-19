package th.co.scb.ace.demo.recovery.architecture.migration;

/**
 * SPEC-RWB-E1-044-007 view (c): a statement cut from the identifier text at a top-level {@code ;}.
 * {@code startOffset} is the first non-blank character, so a leading comment never supplies the
 * kind or the line.
 */
public record MigrationStatement(int startOffset, int endOffset, int startLine, String firstWord, String kind) {
}
