// Recovery Workbench, local end-to-end build.
// Mirrors the ACE monorepo backend layout so recovery module code moves across unchanged:
// package th.co.scb.ace.demo.recovery, migrations in db/modulemigration/recovery/.
// Versions are pinned here. A version change follows CTX-BE-GAP-04 (record it in Environment Design).

plugins {
	java
	jacoco
	id("org.springframework.boot") version "4.1.2"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "th.co.scb.ace"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(21)
	}
}

repositories {
	mavenCentral()
}

extra["springModulithVersion"] = "2.1.1"
val droolsVersion = "10.2.0"          // ADR-012: KIE runtime libraries only
val temporalVersion = "1.41.1"        // ADR-011: Temporal Java SDK
val azureBlobVersion = "12.37.2"      // ADR-007: document hub on Blob storage
val azureIdentityVersion = "1.19.0"
val archunitVersion = "1.5.1"
val restAssuredVersion = "6.3.0"

dependencies {
	// Spring platform (ACE baseline set)
	implementation("org.springframework.boot:spring-boot-starter-actuator")
	implementation("org.springframework.boot:spring-boot-starter-batch")
	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
	implementation("org.springframework.boot:spring-boot-starter-flyway")
	implementation("org.springframework.boot:spring-boot-starter-opentelemetry")
	implementation("org.springframework.boot:spring-boot-starter-quartz")
	implementation("org.springframework.boot:spring-boot-starter-security")
	implementation("org.springframework.boot:spring-boot-starter-security-oauth2-resource-server")
	implementation("org.springframework.boot:spring-boot-starter-validation")
	implementation("org.springframework.boot:spring-boot-starter-webmvc")
	implementation("org.flywaydb:flyway-database-postgresql")
	implementation("org.springframework.modulith:spring-modulith-starter-core")
	implementation("org.springframework.modulith:spring-modulith-starter-jpa")

	// Rules: embedded Drools, no KIE Server, no Business Central, no KJAR (ADR-012)
	implementation("org.drools:drools-engine:$droolsVersion")
	implementation("org.drools:drools-mvel:$droolsVersion")
	implementation("org.drools:drools-decisiontables:$droolsVersion")
	implementation("org.drools:drools-xml-support:$droolsVersion")

	// Workflow: Temporal SDK, worker started only when rwb.p3.temporal is on (ADR-011)
	implementation("io.temporal:temporal-sdk:$temporalVersion")

	// Documents: Azure Blob (Azurite locally). Spring Cloud Azure does not support Boot 4.1 yet,
	// so the SDK is wired directly in DocumentStorageConfig.
	implementation("com.azure:azure-storage-blob:$azureBlobVersion")
	implementation("com.azure:azure-identity:$azureIdentityVersion")

	runtimeOnly("io.micrometer:micrometer-registry-prometheus")
	runtimeOnly("org.postgresql:postgresql")
	runtimeOnly("org.springframework.modulith:spring-modulith-runtime")

	testImplementation("org.springframework.boot:spring-boot-starter-actuator-test")
	testImplementation("org.springframework.boot:spring-boot-starter-batch-test")
	testImplementation("org.springframework.boot:spring-boot-starter-data-jpa-test")
	testImplementation("org.springframework.boot:spring-boot-starter-flyway-test")
	testImplementation("org.springframework.boot:spring-boot-starter-quartz-test")
	testImplementation("org.springframework.boot:spring-boot-starter-security-oauth2-resource-server-test")
	testImplementation("org.springframework.boot:spring-boot-starter-security-test")
	testImplementation("org.springframework.boot:spring-boot-starter-validation-test")
	testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")
	testImplementation("org.springframework.boot:spring-boot-testcontainers")
	testImplementation("org.springframework.modulith:spring-modulith-starter-test")
	testImplementation("org.testcontainers:testcontainers-junit-jupiter")
	testImplementation("org.testcontainers:testcontainers-postgresql")
	testImplementation("io.temporal:temporal-testing:$temporalVersion")
	testImplementation("com.tngtech.archunit:archunit-junit5:$archunitVersion")
	testImplementation("io.rest-assured:rest-assured:$restAssuredVersion")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

dependencyManagement {
	imports {
		mavenBom("org.springframework.modulith:spring-modulith-bom:${property("springModulithVersion")}")
	}
}

// ---------------------------------------------------------------------------------------------
// Test tasks (testing-standards §1, D-RCV-44)
//   test                     unit tests, part of `check`
//   recoveryIntegrationTest  @Tag("recovery-it") Testcontainers tests, outside `check`,
//                            fail (not skip) when Docker is absent
//   e2eTest                  @Tag("e2e") tests against the running docker compose stack
// ---------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------
// Generated typed keys (RWB-E1-042 SPEC-005): one ParameterKey<T> constant per catalog row.
// Build-script code, outside the coverage bundle (D-RCV-40, A-38). The output is checked by
// ParameterKeysGenerationTest (TC-42) and by the catalog migration drift test (TC-27).
// ---------------------------------------------------------------------------------------------
val parameterCatalogFile = layout.projectDirectory.file("src/main/resources/config/parameter-catalog.csv")

val generatedParameterKeysDir = layout.buildDirectory.dir("generated/sources/parameterKeys")

val generateParameterKeys by tasks.registering {
	description = "Generates ParameterKeys.java from config/parameter-catalog.csv."
	group = "build"
	val catalogOverride = providers.gradleProperty("parameterCatalog").map { layout.projectDirectory.file(it) }
	inputs.file(catalogOverride.orElse(parameterCatalogFile))
	outputs.dir(generatedParameterKeysDir)
	doLast {
		fun rows(text: String): List<List<String>> {
			val out = mutableListOf<List<String>>()
			var fields = mutableListOf<String>()
			val cell = StringBuilder()
			var quoted = false
			var i = 0
			while (i < text.length) {
				val c = text[i]
				if (quoted) {
					if (c == '"' && i + 1 < text.length && text[i + 1] == '"') {
						cell.append('"'); i += 2; continue
					}
					if (c == '"') { quoted = false; i++; continue }
					cell.append(c); i++; continue
				}
				when (c) {
					'"' -> { quoted = true; i++ }
					',' -> { fields.add(cell.toString()); cell.setLength(0); i++ }
					'\r' -> {
						if (i + 1 < text.length && text[i + 1] == '\n') i += 2 else i++
						fields.add(cell.toString()); cell.setLength(0)
						out.add(fields); fields = mutableListOf()
					}
					'\n' -> {
						i++
						fields.add(cell.toString()); cell.setLength(0)
						out.add(fields); fields = mutableListOf()
					}
					else -> { cell.append(c); i++ }
				}
			}
			if (cell.isNotEmpty() || fields.isNotEmpty()) {
				fields.add(cell.toString())
				out.add(fields)
			}
			return out.filter { row -> row.any { it.isNotBlank() } }
		}

		fun javaType(valueType: String): String = when (valueType) {
			"INTEGER" -> "Integer"
			"DECIMAL" -> "BigDecimal"
			"BOOLEAN" -> "Boolean"
			"DATE" -> "LocalDate"
			"TIME" -> "LocalTime"
			"DURATION" -> "Duration"
			"CODE_LIST" -> "List<String>"
			else -> "String"
		}

		fun classLiteral(valueType: String): String = when (valueType) {
			"INTEGER" -> "Integer.class"
			"DECIMAL" -> "BigDecimal.class"
			"BOOLEAN" -> "Boolean.class"
			"DATE" -> "LocalDate.class"
			"TIME" -> "LocalTime.class"
			"DURATION" -> "Duration.class"
			"CODE_LIST" -> "(Class<List<String>>) (Class<?>) List.class"
			else -> "String.class"
		}

		fun literal(text: String): String {
			val escaped = StringBuilder("\"")
			for (character in text) {
				when (character) {
					'\\' -> escaped.append("\\\\")
					'"' -> escaped.append("\\\"")
					'\n' -> escaped.append("\\n")
					'\r' -> escaped.append("\\r")
					'\t' -> escaped.append("\\t")
					else -> if (character < ' ') {
						escaped.append(String.format("\\u%04x", character.code))
					}
					else {
						escaped.append(character)
					}
				}
			}
			return escaped.append('"').toString()
		}

		fun constantName(key: String): String =
			key.uppercase().replace('.', '_').replace('-', '_')

		// SEC-042-02: the generated class is compiled before any test runs, so the generator validates
		// every row itself and fails with the row number instead of emitting compilable nonsense.
		fun require(condition: Boolean, row: Int, column: String, rule: String) {
			if (!condition) {
				throw GradleException(
					"parameter-catalog.csv row $row column '$column' violates $rule; fix the catalog file")
			}
		}

		val kinds = setOf("BUSINESS", "ENVIRONMENT")
		val valueTypes = setOf("STRING", "INTEGER", "DECIMAL", "BOOLEAN", "DATE", "TIME", "DURATION", "CODE",
			"CODE_LIST", "JSON")
		val scopes = setOf("GLOBAL", "PRODUCT")
		val valueSources = setOf("TABLE", "ENV", "SECRET")
		val keyPattern = Regex("^[A-Za-z][A-Za-z0-9_.-]{0,99}$")

		val parsed = rows(catalogOverride.orElse(parameterCatalogFile).get().asFile.readText(Charsets.UTF_8))
		require(parsed.size > 1) { "parameter-catalog.csv has no data rows" }
		// REVIEW-001 L9: cells are trimmed once, so the code is generated from the value that was validated.
		val constants = parsed.drop(1).map { row -> row.map { it.trim() } }
		val source = StringBuilder()
		source.append("package th.co.scb.ace.demo.recovery.casewf.config.api;\n\n")
		source.append("import java.math.BigDecimal;\n")
		source.append("import java.time.Duration;\n")
		source.append("import java.time.LocalDate;\n")
		source.append("import java.time.LocalTime;\n")
		source.append("import java.util.List;\n")
		source.append("import java.util.Optional;\n\n")
		source.append("/**\n")
		source.append(" * Generated from {@code backend/src/main/resources/config/parameter-catalog.csv}.\n")
		source.append(" * Do not edit: change the catalog file and rebuild (RWB-E1-042 SPEC-005).\n")
		source.append(" */\n")
		source.append("@SuppressWarnings(\"unchecked\")\n")
		source.append("public final class ParameterKeys {\n\n")
		val seenConstants = mutableSetOf<String>()
		for ((index, row) in constants.withIndex()) {
			val rowNumber = index + 2
			require(row.size == 16, rowNumber, "row", "the sixteen columns of §7.1")
			val key = row[0].trim()
			require(keyPattern.matches(key), rowNumber, "key", "the key pattern")
			require(kinds.contains(row[1].trim()), rowNumber, "kind", "BUSINESS or ENVIRONMENT")
			require(valueTypes.contains(row[2].trim()), rowNumber, "value_type", "one of the ten types")
			require(scopes.contains(row[7].trim()), rowNumber, "scope", "GLOBAL or PRODUCT")
			require(row[8].trim() == "true" || row[8].trim() == "false", rowNumber, "required", "true or false")
			require(row[12].trim() == "true" || row[12].trim() == "false", rowNumber, "secret", "true or false")
			require(valueSources.contains(row[13].trim()), rowNumber, "value_source", "TABLE, ENV or SECRET")
			require(seenConstants.add(constantName(key)), rowNumber, "key", "a unique constant name")
		}
		for (row in constants) {
			val key = row[0]
			val type = javaType(row[2])
			val environments = row[10].split(",").filter { it.isNotBlank() }.joinToString(", ") { literal(it.trim()) }
			val usedBy = row[11].split(";").filter { it.isNotBlank() }.joinToString(", ") { literal(it.trim()) }
			source.append("\tpublic static final ParameterKey<$type> ${constantName(key)} = new ParameterKey<$type>(\n")
			source.append("\t\t\t${literal(key)}, ${classLiteral(row[2])}, ${literal(row[1])}, ${literal(row[3])},\n")
			source.append("\t\t\t${literal(row[4])}, ${literal(row[5])}, ")
			source.append(if (row[6].isEmpty()) "null" else literal(row[6]))
			source.append(", ${literal(row[7])}, ${row[8].trim()},\n")
			source.append("\t\t\t${literal(row[9])}, List.of($environments), List.of($usedBy), ${row[12].trim()},\n")
			source.append("\t\t\t${literal(row[13])}, ")
			source.append(if (row[14].isEmpty()) "null" else literal(row[14]))
			source.append(", ${literal(row[15])});\n\n")
		}
		source.append("\tprivate static final List<ParameterKey<?>> ALL = List.of(\n")
		source.append(constants.joinToString(",\n") { "\t\t\t${constantName(it[0])}" })
		source.append(");\n\n")
		source.append("\tprivate ParameterKeys() {\n\t}\n\n")
		source.append("\t/** Every catalog row, in file order. */\n")
		source.append("\tpublic static List<ParameterKey<?>> all() {\n\t\treturn ALL;\n\t}\n\n")
		source.append("\t/** The constant for a key and type; empty when the key is absent or its type differs. */\n")
		source.append("\tpublic static <T> Optional<ParameterKey<T>> byName(String key, Class<T> type) {\n")
		source.append("\t\tfor (ParameterKey<?> candidate : ALL) {\n")
		source.append("\t\t\tif (candidate.name().equals(key) && candidate.type().equals(type)) {\n")
		source.append("\t\t\t\treturn Optional.of((ParameterKey<T>) candidate);\n")
		source.append("\t\t\t}\n\t\t}\n")
		source.append("\t\treturn Optional.empty();\n\t}\n}\n")

		val output = generatedParameterKeysDir.get()
			.file("th/co/scb/ace/demo/recovery/casewf/config/api/ParameterKeys.java").asFile
		output.parentFile.mkdirs()
		output.writeText(source.toString(), Charsets.UTF_8)
	}
}

sourceSets.main {
	java.srcDir(generatedParameterKeysDir)
}

tasks.named<JavaCompile>("compileJava") {
	dependsOn(generateParameterKeys)
}

tasks.withType<Test>().configureEach {
	useJUnitPlatform()
	systemProperty("user.timezone", "Asia/Bangkok")
}

tasks.named<Test>("test") {
	useJUnitPlatform { excludeTags("recovery-it", "e2e") }
	finalizedBy("recoveryCoverageReport")
}

val recoveryIntegrationTest by tasks.registering(Test::class) {
	description = "Recovery Testcontainers integration tests (@Tag recovery-it)."
	group = "verification"
	testClassesDirs = sourceSets.test.get().output.classesDirs
	classpath = sourceSets.test.get().runtimeClasspath
	useJUnitPlatform { includeTags("recovery-it") }
	systemProperty("recovery.it.requireDocker", "true")
	shouldRunAfter(tasks.named("test"))
}

val e2eTest by tasks.registering(Test::class) {
	description = "End-to-end tests against the local stack (docker compose up first)."
	group = "verification"
	testClassesDirs = sourceSets.test.get().output.classesDirs
	classpath = sourceSets.test.get().runtimeClasspath
	useJUnitPlatform { includeTags("e2e") }
	systemProperty("rwb.e2e.baseUrl", System.getenv("RWB_E2E_BASE_URL") ?: "http://localhost:8080")
	systemProperty("rwb.e2e.oidcUrl", System.getenv("RWB_E2E_OIDC_URL") ?: "http://localhost:8090/entra")
}

// Coverage on recovery packages plus the test-scope boundary tooling, 80% on four counters
// (BS-7.2; RWB-TE-001 SPEC-020). Fixtures and *Test classes are not measured.
val recoveryClasses = files(sourceSets.main.get().output.classesDirs.map {
	fileTree(it) { include("th/co/scb/ace/demo/recovery/**") }
})

val boundaryToolingClasses = files(sourceSets.test.get().output.classesDirs.map {
	fileTree(it) {
		include("th/co/scb/ace/demo/recovery/architecture/boundary/**")
		exclude("**/*Test.class", "**/*Test$*.class")
	}
})

// RWB-E1-044 SPEC-014 case 1: this story's test-scope tooling joins the same combined bundle.
val migrationToolingClasses = files(sourceSets.test.get().output.classesDirs.map {
	fileTree(it) {
		include("th/co/scb/ace/demo/recovery/architecture/migration/**")
		exclude("**/*Test.class", "**/*Test$*.class", "**/*IT.class", "**/*IT$*.class")
	}
})

// RWB-E1-042 SPEC-014 and §12.11: the two build checks' logic joins the same combined bundle.
val parameterToolingClasses = files(sourceSets.test.get().output.classesDirs.map {
	fileTree(it) {
		include("th/co/scb/ace/demo/recovery/architecture/parameters/**")
		exclude("**/*Test.class", "**/*Test$*.class", "**/*IT.class", "**/*IT$*.class")
	}
})

val recoveryCoverageReport by tasks.registering(JacocoReport::class) {
	description = "JaCoCo report for th.co.scb.ace.demo.recovery and the test-scope tooling."
	group = "verification"
	executionData(tasks.named("test").get())
	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses, migrationToolingClasses,
		parameterToolingClasses)
	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
	reports {
		xml.required = true
		xml.outputLocation = layout.buildDirectory.file("reports/jacoco/recoveryCoverageReport.xml")
		html.required = true
	}
}

val recoveryCoverageVerification by tasks.registering(JacocoCoverageVerification::class) {
	description = "Fails below 80% line, instruction, branch or method coverage on recovery packages and the test-scope tooling."
	group = "verification"
	executionData(tasks.named("test").get())
	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses, migrationToolingClasses,
		parameterToolingClasses)
	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
	violationRules {
		rule {
			limit { counter = "LINE"; minimum = "0.80".toBigDecimal() }
			limit { counter = "INSTRUCTION"; minimum = "0.80".toBigDecimal() }
			limit { counter = "BRANCH"; minimum = "0.80".toBigDecimal() }
			limit { counter = "METHOD"; minimum = "0.80".toBigDecimal() }
		}
	}
}

// ---------------------------------------------------------------------------------------------
// RWB-TE-002 code owners validation (SPEC-013, SPEC-014). Defined here, run on the host.
//   codeOwnersTest                  JUnit tag "codeowners", also run by `test`
//   codeOwnersCoverageReport        JaCoCo report for the codeowners package
//   codeOwnersCoverageVerification  80% LINE, BRANCH, INSTRUCTION, METHOD
// ---------------------------------------------------------------------------------------------
val repositoryRoot = requireNotNull(rootDir.parentFile) { "RWB-TE-002: backend/ must sit in the repository root" }

val codeOwnersGovernanceInputs = files(
	repositoryRoot.resolve(".gitlab/CODEOWNERS"),
	repositoryRoot.resolve(".gitlab/codeowners-register.yaml"),
	repositoryRoot.resolve(".gitlab/host-settings.md"),
	repositoryRoot.resolve(".gitlab/merge_request_templates/Default.md"),
	repositoryRoot.resolve("AGENTS.md"),
	repositoryRoot.resolve(".gitlab-ci.yml")
)

val codeOwnersTest by tasks.registering(Test::class) {
	description = "RWB-TE-002 code owners and governance tests (@Tag codeowners)."
	group = "verification"
	inputs.files(codeOwnersGovernanceInputs)
	testClassesDirs = sourceSets.test.get().output.classesDirs
	classpath = sourceSets.test.get().runtimeClasspath
	useJUnitPlatform { includeTags("codeowners") }
	// The tests read the whole repository tree (UT-26, V10), which no input list can cover: always re-run.
	outputs.upToDateWhen { false }
	finalizedBy("codeOwnersCoverageReport")
}

tasks.named<Test>("test") {
	inputs.files(codeOwnersGovernanceInputs)
}

val codeOwnersClasses = files(sourceSets.test.get().output.classesDirs.map {
	fileTree(it) {
		include("th/co/scb/ace/demo/recovery/architecture/codeowners/**")
		exclude("**/*Test.class", "**/*Test\$*.class")
	}
})

val codeOwnersCoverageReport by tasks.registering(JacocoReport::class) {
	description = "JaCoCo report for the RWB-TE-002 codeowners package."
	group = "verification"
	executionData(tasks.named("codeOwnersTest").get())
	classDirectories.setFrom(codeOwnersClasses)
	sourceDirectories.setFrom(sourceSets.test.get().java.srcDirs)
	reports {
		xml.required = true
		xml.outputLocation = layout.buildDirectory.file("reports/jacoco/codeOwnersCoverageReport.xml")
		html.required = true
	}
}

val codeOwnersCoverageVerification by tasks.registering(JacocoCoverageVerification::class) {
	description = "Fails below 80% line, branch, instruction or method coverage on the RWB-TE-002 codeowners package."
	group = "verification"
	dependsOn(tasks.named("codeOwnersTest"))
	executionData(tasks.named("codeOwnersTest").get())
	classDirectories.setFrom(codeOwnersClasses)
	sourceDirectories.setFrom(sourceSets.test.get().java.srcDirs)
	violationRules {
		rule {
			limit { counter = "LINE"; minimum = "0.80".toBigDecimal() }
			limit { counter = "BRANCH"; minimum = "0.80".toBigDecimal() }
			limit { counter = "INSTRUCTION"; minimum = "0.80".toBigDecimal() }
			limit { counter = "METHOD"; minimum = "0.80".toBigDecimal() }
		}
	}
}