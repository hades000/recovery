package th.co.scb.ace.demo.recovery.casewf.rules;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;
import java.util.Map;

import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;
import th.co.scb.ace.demo.recovery.casewf.rules.CompiledRulePackage;
import th.co.scb.ace.demo.recovery.casewf.rules.RuleEngine.RuleCompilationException;
import th.co.scb.ace.demo.recovery.casewf.rules.RuleInput;
import th.co.scb.ace.demo.recovery.casewf.rules.RuleResult;

/**
 * Compiles a Drools XLSX decision table in the ADR-012 shape (RuleSet = package code, NAME = rule
 * ID, one activation group, priority from row order, default row last) and evaluates it.
 * The rows are synthetic: they are not the bank's ENTRY rules.
 */
class DroolsRuleEngineTest {

	private final DroolsRuleEngine engine = new DroolsRuleEngine(new DroolsProperties(2), new SimpleMeterRegistry(),
			new RecoveryFlags(false, true));

	@Test
	void compilesWorkbookAndFirstMatchDecides() throws IOException {
		CompiledRulePackage pkg = engine.compile("TEST_ENTRY", "v1", "TEST_ENTRY.xlsx", workbook(List.of(
				new String[] { "T-ENTRY-01", "entry", "100", "90", "SECURED", "Q-LEGAL" },
				new String[] { "T-ENTRY-02", "entry", "90", "90", "", "Q-RECOVERY" },
				new String[] { "T-ENTRY-99", "entry", "1", "", "", "Q-HOLD" })));

		assertThat(pkg.ruleIds()).containsExactly("T-ENTRY-01", "T-ENTRY-02", "T-ENTRY-99");
		assertThat(pkg.drlSha256()).hasSize(64);
		assertThat(pkg.drlSource()).contains("package TEST_ENTRY").contains("activation-group \"entry\"");

		RuleResult secured = engine.evaluate("TEST_ENTRY", "v1", RuleInput.of(Map.of("dpd", 120, "productGroup", "SECURED")));
		assertThat(secured.ruleId()).isEqualTo("T-ENTRY-01");
		assertThat(secured.packageVersion()).isEqualTo("v1");
		assertThat(secured.outputs()).containsEntry("targetQueue", "Q-LEGAL");

		RuleResult unsecured = engine.evaluate("TEST_ENTRY", "v1", RuleInput.of(Map.of("dpd", 95, "productGroup", "CARD")));
		assertThat(unsecured.ruleId()).isEqualTo("T-ENTRY-02");

		RuleResult fallback = engine.evaluate("TEST_ENTRY", "v1", RuleInput.of(Map.of("dpd", 30, "productGroup", "CARD")));
		assertThat(fallback.ruleId()).isEqualTo("T-ENTRY-99");
		assertThat(fallback.outputs()).containsEntry("targetQueue", "Q-HOLD");
	}

	@Test
	void versionsAreKeptApart() throws IOException {
		engine.compile("TEST_ENTRY", "v1", "a.xlsx", workbook(List.<String[]>of(new String[] { "T-A", "entry", "1", "", "", "Q-ONE" })));
		engine.compile("TEST_ENTRY", "v2", "b.xlsx", workbook(List.<String[]>of(new String[] { "T-B", "entry", "1", "", "", "Q-TWO" })));

		RuleInput input = RuleInput.of(Map.of("dpd", 1));
		assertThat(engine.evaluate("TEST_ENTRY", "v1", input).outputs()).containsEntry("targetQueue", "Q-ONE");
		assertThat(engine.evaluate("TEST_ENTRY", "v2", input).outputs()).containsEntry("targetQueue", "Q-TWO");
	}

	@Test
	void cacheEvictsLeastRecentlyUsedVersion() throws IOException {
		byte[] wb = workbook(List.<String[]>of(new String[] { "T-A", "entry", "1", "", "", "Q" }));
		engine.compile("P", "v1", "p.xlsx", wb);
		engine.compile("P", "v2", "p.xlsx", wb);
		engine.compile("P", "v3", "p.xlsx", wb); // cache max is 2

		assertThatThrownBy(() -> engine.evaluate("P", "v1", RuleInput.of(Map.of("dpd", 1))))
				.isInstanceOf(IllegalStateException.class).hasMessageContaining("not loaded");
	}

	@Test
	void brokenWorkbookIsRefused() throws IOException {
		byte[] broken = workbook(List.<String[]>of(new String[] { "T-BAD", "entry", "1", "abc", "", "Q" }), "num(\"dpd\") >=== $param");
		assertThatThrownBy(() -> engine.compile("BROKEN", "v1", "broken.xlsx", broken))
				.isInstanceOf(RuleCompilationException.class)
				.satisfies(ex -> assertThat(((RuleCompilationException) ex).messages()).isNotEmpty());
	}

	static byte[] workbook(List<String[]> rows) throws IOException {
		return workbook(rows, "num(\"dpd\").intValue() >= $param");
	}

	/** Builds a decision table in the Drools XLS layout, the format RW-COE authors in Excel. */
	static byte[] workbook(List<String[]> rows, String dpdCondition) throws IOException {
		try (XSSFWorkbook wb = new XSSFWorkbook(); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			Sheet sheet = wb.createSheet("Entry");
			int r = 0;
			row(sheet, r++, "RuleSet", "TEST_ENTRY");
			row(sheet, r++, "Import", "th.co.scb.ace.demo.recovery.casewf.rules.RuleInput, th.co.scb.ace.demo.recovery.casewf.rules.RuleOutcome");
			row(sheet, r++, "Variables", "th.co.scb.ace.demo.recovery.casewf.rules.RuleOutcome outcome");
			r++;
			row(sheet, r++, "RuleTable Entry");
			row(sheet, r++, "NAME", "ACTIVATION-GROUP", "PRIORITY", "CONDITION", "CONDITION", "ACTION");
			// One pattern over both condition columns: the type cell is merged across them, as in Excel.
			int typeRow = r;
			row(sheet, r++, "", "", "", "$in : RuleInput", "", "");
			sheet.addMergedRegion(new CellRangeAddress(typeRow, typeRow, 4, 5));
			row(sheet, r++, "", "", "", dpdCondition, "text(\"productGroup\") == \"$param\"",
					"outcome.decide(drools.getRule().getName()); outcome.put(\"targetQueue\", \"$param\");");
			row(sheet, r++, "Rule ID", "Group", "Priority", "DPD at least", "Product group", "Target queue");
			for (String[] data : rows) {
				row(sheet, r++, data);
			}
			wb.write(out);
			return out.toByteArray();
		}
	}

	private static void row(Sheet sheet, int index, String... values) {
		Row row = sheet.createRow(index);
		for (int c = 0; c < values.length; c++) {
			var cell = row.createCell(c + 1); // Drools tables start in column B
			if (!values[c].isEmpty()) {
				cell.setCellValue(values[c]);
			}
		}
	}
}
