package th.co.scb.ace.demo.recovery.casewf.rules;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Collections;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.drools.decisiontable.InputType;
import org.drools.decisiontable.SpreadsheetCompiler;
import org.kie.api.KieBase;
import org.kie.api.builder.Message;
import org.kie.api.io.ResourceType;
import org.kie.api.runtime.StatelessKieSession;
import org.kie.internal.utils.KieHelper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;

/**
 * Embedded Drools, KIE runtime libraries only: no KIE Server, no Business Central, no KJAR
 * (ADR-012, BS-6.4). A workbook is compiled to DRL with the decision-table compiler, the DRL to a
 * KieBase, and the KieBase is cached per package version (LRU, {@code rwb.drools.kiebase-cache-max}).
 *
 * <p>Locally the cache is the only store. The rule package story (E1-073) loads versions from
 * {@code rule_package_version} on a cache miss and refuses a version whose DRL checksum differs.
 */
@Component
@ConditionalOnProperty(name = "rwb.p3.drools", havingValue = "true")
class DroolsRuleEngine implements RuleEngine {

	private static final Logger log = LoggerFactory.getLogger(DroolsRuleEngine.class);
	private static final Pattern RULE_NAME = Pattern.compile("^rule\\s+\"([^\"]+)\"", Pattern.MULTILINE);

	private final Map<String, KieBase> cache;
	private final Timer evaluationTimer;

	DroolsRuleEngine(DroolsProperties properties, MeterRegistry meters, RecoveryFlags flags) {
		int max = properties.kiebaseCacheMax();
		this.cache = Collections.synchronizedMap(new LinkedHashMap<>(16, 0.75f, true) {
			@Override
			protected boolean removeEldestEntry(Map.Entry<String, KieBase> eldest) {
				return size() > max;
			}
		});
		this.evaluationTimer = Timer.builder("rwb.drools.evaluation").description("Drools evaluation time")
				.register(meters);
		log.info("Drools rule engine enabled (rwb.p3.drools={}), KieBase cache max {}", flags.drools(), max);
	}

	@Override
	public CompiledRulePackage compile(String packageCode, String versionLabel, String fileName, byte[] workbook) {
		InputType type = fileName.toLowerCase().endsWith(".csv") ? InputType.CSV : InputType.XLS;
		String drl;
		try {
			drl = new SpreadsheetCompiler().compile(new ByteArrayInputStream(workbook), type);
		}
		catch (RuntimeException ex) {
			throw new RuleCompilationException(packageCode, List.of(String.valueOf(ex.getMessage())));
		}

		KieHelper helper = new KieHelper();
		helper.addContent(drl, ResourceType.DRL);
		List<String> errors = helper.verify().getMessages(Message.Level.ERROR).stream().map(Message::getText).toList();
		if (!errors.isEmpty()) {
			throw new RuleCompilationException(packageCode, errors);
		}
		KieBase kieBase = helper.build();
		cache.put(key(packageCode, versionLabel), kieBase);

		return new CompiledRulePackage(packageCode, versionLabel, drl, sha256(drl), ruleIds(drl));
	}

	@Override
	public RuleResult evaluate(String packageCode, String versionLabel, RuleInput input) {
		KieBase kieBase = cache.get(key(packageCode, versionLabel));
		if (kieBase == null) {
			throw new IllegalStateException("Rule package version not loaded: " + packageCode + " " + versionLabel);
		}
		return evaluationTimer.record(() -> {
			StatelessKieSession session = kieBase.newStatelessKieSession();
			RuleOutcome outcome = new RuleOutcome();
			session.setGlobal("outcome", outcome);
			session.execute(input);
			return outcome.ruleId() == null
					? RuleResult.noMatch(packageCode, versionLabel)
					: new RuleResult(packageCode, versionLabel, outcome.ruleId(), outcome.outputs());
		});
	}

	private static String key(String packageCode, String versionLabel) {
		return packageCode + "@" + versionLabel;
	}

	private static List<String> ruleIds(String drl) {
		Matcher m = RULE_NAME.matcher(drl);
		List<String> ids = new java.util.ArrayList<>();
		while (m.find()) {
			ids.add(m.group(1));
		}
		return ids;
	}

	private static String sha256(String text) {
		try {
			return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(text.getBytes(StandardCharsets.UTF_8)));
		}
		catch (NoSuchAlgorithmException ex) {
			throw new IllegalStateException(ex);
		}
	}
}
