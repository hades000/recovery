package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.flywaydb.core.Flyway;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;

import th.co.scb.ace.demo.recovery.architecture.parameters.CatalogFileParser;
import th.co.scb.ace.demo.recovery.architecture.parameters.CatalogRow;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;

/**
 * TC-E1-042-13, TC-E1-042-14 and TC-E1-042-27 (SPEC-RWB-E1-042-001, -002, -006): the migration applies
 * on an empty schema and on a schema built from Physical Schema v6, both tables carry every v6 column
 * in its v6 position with its v6 type, width, nullability and default, the 19 catalog rows and the 40
 * value rows are seeded, and the persisted catalog equals the generated keys row for row.
 *
 * <p>Runs in {@code recoveryIntegrationTest}; it fails without Docker (D-RCV-44).
 */
@Tag("recovery-it")
@Testcontainers
class ParameterMigrationIT {

	private static final String SEED_IDENTITY = "00000000-0000-0000-0000-0000000e1042";

	private static final Path MIGRATIONS = Path.of("src/main/resources/db/modulemigration/recovery");

	@Container
	static final PostgreSQLContainer POSTGRES = new PostgreSQLContainer("postgres:16.16-alpine");

	private static String url() {
		return "jdbc:postgresql://" + POSTGRES.getHost() + ":" + POSTGRES.getMappedPort(5432) + "/"
				+ POSTGRES.getDatabaseName();
	}

	private static Connection connect() throws SQLException {
		return DriverManager.getConnection(url(), POSTGRES.getUsername(), POSTGRES.getPassword());
	}

	private static void migrate(String schema) {
		Flyway.configure()
			.dataSource(url(), POSTGRES.getUsername(), POSTGRES.getPassword())
			.schemas(schema)
			.defaultSchema(schema)
			.table("flyway_schema_history_recovery")
			.locations("filesystem:" + MIGRATIONS.toAbsolutePath())
			.placeholders(Map.of("recoverySchema", schema))
			.cleanDisabled(true)
			.baselineOnMigrate(true)
			.baselineVersion("0")
			.createSchemas(true)
			.load()
			.migrate();
	}

	private static void execute(String sql) throws SQLException {
		try (Connection connection = connect(); Statement statement = connection.createStatement()) {
			statement.execute(sql);
		}
	}

	/** One information_schema.columns row, reduced to the fields TC-13 asserts. */
	private record Column(String name, String type, Integer length, String nullable, String dflt) {
	}

	private static List<Column> columns(String schema, String table) throws SQLException {
		List<Column> columns = new ArrayList<>();
		try (Connection connection = connect();
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery("""
						SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
						FROM information_schema.columns
						WHERE table_schema = '%s' AND table_name = '%s'
						ORDER BY ordinal_position""".formatted(schema, table))) {
			while (rows.next()) {
				columns.add(new Column(rows.getString(1), rows.getString(2), (Integer) rows.getObject(3),
						rows.getString(4), rows.getString(5)));
			}
		}
		return columns;
	}

	private static Integer count(String schema, String table) throws SQLException {
		try (Connection connection = connect();
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery(
						"SELECT count(*) FROM " + schema + "." + table)) {
			rows.next();
			return rows.getInt(1);
		}
	}

	private static List<String> names(String sql) throws SQLException {
		List<String> names = new ArrayList<>();
		try (Connection connection = connect();
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery(sql)) {
			while (rows.next()) {
				names.add(rows.getString(1));
			}
		}
		return names;
	}

	private static void assertCatalogColumns(String schema) throws SQLException {
		List<Column> columns = columns(schema, "parameter_catalog");
		assertThat(columns).hasSize(22);
		assertThat(columns).extracting(Column::name).containsExactly("id", "param_key", "kind", "value_type", "unit",
				"min_value", "max_value", "default_value", "scope", "required", "owner_role", "environments", "used_by",
				"secret", "description", "is_active", "state", "version", "created_at", "created_by", "updated_at",
				"updated_by");
		assertColumn(columns, "id", "uuid", null, "NO", "gen_random_uuid");
		assertColumn(columns, "param_key", "character varying", 100, "NO", null);
		assertColumn(columns, "kind", "character varying", 15, "NO", null);
		assertColumn(columns, "value_type", "character varying", 15, "NO", null);
		assertColumn(columns, "unit", "character varying", 20, "YES", null);
		assertColumn(columns, "min_value", "character varying", 40, "YES", null);
		assertColumn(columns, "max_value", "character varying", 40, "YES", null);
		assertColumn(columns, "default_value", "character varying", 400, "YES", null);
		assertColumn(columns, "scope", "character varying", 10, "NO", "GLOBAL");
		assertColumn(columns, "required", "boolean", null, "NO", "false");
		assertColumn(columns, "owner_role", "character varying", 20, "NO", null);
		assertColumn(columns, "environments", "character varying", 40, "YES", null);
		assertColumn(columns, "used_by", "character varying", 400, "YES", null);
		assertColumn(columns, "secret", "boolean", null, "NO", "false");
		assertColumn(columns, "description", "character varying", 400, "NO", null);
		assertColumn(columns, "is_active", "boolean", null, "NO", "true");
		assertColumn(columns, "state", "character varying", 40, "YES", null);
		assertColumn(columns, "version", "integer", null, "NO", "1");
		assertColumn(columns, "created_at", "timestamp with time zone", null, "NO", "now()");
		assertColumn(columns, "created_by", "uuid", null, "YES", null);
		assertColumn(columns, "updated_at", "timestamp with time zone", null, "NO", "now()");
		assertColumn(columns, "updated_by", "uuid", null, "YES", null);
	}

	private static void assertValueColumns(String schema) throws SQLException {
		List<Column> columns = columns(schema, "parameter_value");
		assertThat(columns).hasSize(22);
		assertThat(columns.subList(0, 19)).extracting(Column::name).containsExactly("id", "param_key", "environment",
				"param_value", "product_group", "version_no", "valid_from", "valid_to", "status", "author_user_id",
				"approver_user_id", "approved_at", "is_active", "state", "version", "created_at", "created_by",
				"updated_at", "updated_by");
		assertColumn(columns, "id", "uuid", null, "NO", "gen_random_uuid");
		assertColumn(columns, "param_key", "character varying", 100, "NO", null);
		assertColumn(columns, "environment", "character varying", 4, "NO", null);
		assertColumn(columns, "param_value", "character varying", 400, "NO", null);
		assertColumn(columns, "product_group", "character varying", 15, "YES", null);
		assertColumn(columns, "version_no", "integer", null, "NO", null);
		assertColumn(columns, "valid_from", "date", null, "NO", null);
		assertColumn(columns, "valid_to", "date", null, "YES", null);
		assertColumn(columns, "status", "character varying", 15, "NO", "VALIDATED");
		assertColumn(columns, "author_user_id", "uuid", null, "NO", null);
		assertColumn(columns, "approver_user_id", "uuid", null, "YES", null);
		assertColumn(columns, "approved_at", "timestamp with time zone", null, "YES", null);
		assertColumn(columns, "is_active", "boolean", null, "NO", "true");
		assertColumn(columns, "state", "character varying", 40, "YES", null);
		assertColumn(columns, "version", "integer", null, "NO", "1");
		assertColumn(columns, "created_at", "timestamp with time zone", null, "NO", "now()");
		assertColumn(columns, "created_by", "uuid", null, "YES", null);
		assertColumn(columns, "updated_at", "timestamp with time zone", null, "NO", "now()");
		assertColumn(columns, "updated_by", "uuid", null, "YES", null);
		assertColumn(columns, "load_id", "uuid", null, "YES", null);
		assertColumn(columns, "content_hash", "character", 64, "YES", null);
		assertColumn(columns, "rollback_reason", "character varying", 400, "YES", null);
	}

	private static void assertColumn(List<Column> columns, String name, String type, Integer length, String nullable,
			String defaultFragment) {
		Column column = columns.stream().filter(candidate -> candidate.name().equals(name)).findFirst()
			.orElseThrow(() -> new AssertionError("missing column " + name));
		assertThat(column.type()).as(name + " type").isEqualTo(type);
		assertThat(column.length()).as(name + " length").isEqualTo(length);
		assertThat(column.nullable()).as(name + " nullability").isEqualTo(nullable);
		if (defaultFragment == null) {
			assertThat(column.dflt()).as(name + " default").isNull();
		}
		else {
			assertThat(column.dflt()).as(name + " default").contains(defaultFragment);
		}
	}

	private static void assertConstraintsAndIndexes(String schema) throws SQLException {
		assertThat(names("""
				SELECT conname FROM pg_constraint
				WHERE conrelid IN ('%s.parameter_catalog'::regclass, '%s.parameter_value'::regclass)
				ORDER BY conname""".formatted(schema, schema))).contains("uk_parameter_catalog", "uk_parameter_value",
						"ck_parameter_catalog_scope", "ck_parameter_catalog_kind", "ck_parameter_catalog_value_type",
						"ck_parameter_catalog_environments", "ck_parameter_catalog_secret_default",
						"ck_parameter_value_environment", "ck_parameter_value_status", "ck_parameter_value_dates",
						"ck_parameter_value_version", "ck_parameter_value_maker_checker",
						"ck_parameter_value_approved_at", "ck_parameter_value_load_hash",
						"ck_parameter_value_rollback_reason", "fk_parameter_value_catalog");
		assertThat(names("SELECT indexname FROM pg_indexes WHERE schemaname = '" + schema + "' ORDER BY indexname"))
			.contains("ix_parameter_value_in_force", "ix_parameter_value_load", "ux_parameter_value_version_all",
					"ux_parameter_value_approved_from");
	}

	/** TC-13: an empty schema gets both tables, every v6 column, the constraints, the indexes and the seed. */
	@Test
	void emptySchemaGetsTablesConstraintsIndexesAndSeed() throws SQLException {
		String schema = "migration_empty";
		migrate(schema);

		assertCatalogColumns(schema);
		assertValueColumns(schema);
		assertConstraintsAndIndexes(schema);

		assertThat(count(schema, "parameter_catalog")).isEqualTo(19);
		assertThat(count(schema, "parameter_value")).isEqualTo(40);

		List<Map<String, Object>> seeded = rows(schema, """
				SELECT param_key, environment, status, version_no, author_user_id::text, created_by::text,
				       approver_user_id, is_active, state, version, created_at, content_hash, load_id, rollback_reason
				FROM %s.parameter_value""".formatted(schema));
		assertThat(seeded).hasSize(40);
		for (Map<String, Object> row : seeded) {
			assertThat(row.get("status")).isEqualTo("APPROVED");
			assertThat(row.get("version_no")).isEqualTo(1);
			assertThat(row.get("author_user_id")).isEqualTo(SEED_IDENTITY);
			assertThat(row.get("created_by")).isEqualTo(SEED_IDENTITY);
			assertThat(row.get("approver_user_id")).isNull();
			assertThat(row.get("is_active")).isEqualTo(true);
			assertThat(row.get("state")).isNull();
			assertThat(row.get("version")).isEqualTo(1);
			assertThat(row.get("created_at")).isNotNull();
			assertThat(row.get("content_hash")).isNull();
			assertThat(row.get("load_id")).isNull();
			assertThat(row.get("rollback_reason")).isNull();
			assertThat(row.get("environment")).isIn("DEV", "SIT", "UAT", "PROD");
		}

		List<Map<String, Object>> catalog = rows(schema, """
				SELECT param_key, created_by::text, updated_by::text, is_active, version, state, created_at
				FROM %s.parameter_catalog""".formatted(schema));
		assertThat(catalog).hasSize(19);
		for (Map<String, Object> row : catalog) {
			assertThat(row.get("created_by")).isEqualTo(SEED_IDENTITY);
			assertThat(row.get("updated_by")).isEqualTo(SEED_IDENTITY);
			assertThat(row.get("is_active")).isEqualTo(true);
			assertThat(row.get("version")).isEqualTo(1);
			assertThat(row.get("state")).isNull();
			assertThat(row.get("created_at")).isNotNull();
		}

		// A second start applies nothing.
		migrate(schema);
		assertThat(count(schema, "parameter_catalog")).isEqualTo(19);
		assertThat(count(schema, "parameter_value")).isEqualTo(40);
	}

	/** TC-14: on a schema built from Physical Schema v6 the v6 columns are unchanged and the additions appear. */
	@Test
	void physicalSchemaSixGetsTheAdditions() throws SQLException {
		String schema = "migration_v6";
		execute("CREATE SCHEMA IF NOT EXISTS " + schema);
		execute("""
				CREATE TABLE %s.parameter_catalog (
				    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
				    param_key varchar(100) NOT NULL,
				    kind varchar(15) NOT NULL,
				    value_type varchar(15) NOT NULL,
				    unit varchar(20),
				    min_value varchar(40),
				    max_value varchar(40),
				    default_value varchar(400),
				    scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
				    required boolean NOT NULL DEFAULT false,
				    owner_role varchar(20) NOT NULL,
				    environments varchar(40),
				    used_by varchar(400),
				    secret boolean NOT NULL DEFAULT false,
				    description varchar(400) NOT NULL,
				    is_active boolean NOT NULL DEFAULT true,
				    state varchar(40),
				    version integer NOT NULL DEFAULT 1,
				    created_at timestamptz NOT NULL DEFAULT now(),
				    created_by uuid,
				    updated_at timestamptz NOT NULL DEFAULT now(),
				    updated_by uuid,
				    CONSTRAINT uk_parameter_catalog UNIQUE (param_key)
				)""".formatted(schema));
		execute("""
				CREATE TABLE %s.parameter_value (
				    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
				    param_key varchar(100) NOT NULL,
				    environment varchar(4) NOT NULL,
				    param_value varchar(400) NOT NULL,
				    product_group varchar(15),
				    version_no integer NOT NULL,
				    valid_from date NOT NULL,
				    valid_to date,
				    status varchar(15) NOT NULL DEFAULT 'VALIDATED',
				    author_user_id uuid NOT NULL,
				    approver_user_id uuid,
				    approved_at timestamptz,
				    is_active boolean NOT NULL DEFAULT true,
				    state varchar(40),
				    version integer NOT NULL DEFAULT 1,
				    created_at timestamptz NOT NULL DEFAULT now(),
				    created_by uuid,
				    updated_at timestamptz NOT NULL DEFAULT now(),
				    updated_by uuid,
				    CONSTRAINT uk_parameter_value UNIQUE (param_key, environment, product_group, version_no)
				)""".formatted(schema));

		List<Column> catalogBefore = columns(schema, "parameter_catalog");
		List<Column> valueBefore = columns(schema, "parameter_value");
		assertThat(catalogBefore).hasSize(22);
		assertThat(valueBefore).hasSize(19);

		migrate(schema);

		assertThat(columns(schema, "parameter_catalog")).isEqualTo(catalogBefore);
		assertThat(columns(schema, "parameter_value").subList(0, 19)).isEqualTo(valueBefore);
		assertThat(columns(schema, "parameter_value")).hasSize(22);
		assertThat(columns(schema, "parameter_value").subList(19, 22)).extracting(Column::name)
			.containsExactly("load_id", "content_hash", "rollback_reason");
		assertConstraintsAndIndexes(schema);
		assertThat(count(schema, "parameter_catalog")).isEqualTo(19);
		assertThat(count(schema, "parameter_value")).isEqualTo(40);
	}

	/** TC-27: the persisted catalog equals the generated keys on every mirrored column. */
	@Test
	void catalogTableEqualsTheGeneratedKeys() throws SQLException {
		String schema = "migration_drift";
		migrate(schema);

		List<Map<String, Object>> persisted = rows(schema, """
				SELECT param_key, kind, value_type, coalesce(unit, '') AS unit, coalesce(min_value, '') AS min_value,
				       coalesce(max_value, '') AS max_value, coalesce(default_value, '') AS default_value, scope,
				       required, owner_role, coalesce(environments, '') AS environments, coalesce(used_by, '') AS used_by,
				       secret, description
				FROM %s.parameter_catalog ORDER BY param_key""".formatted(schema));
		assertThat(persisted).hasSize(ParameterKeys.all().size());

		Map<String, Map<String, Object>> byKey = new LinkedHashMap<>();
		for (Map<String, Object> row : persisted) {
			byKey.put((String) row.get("param_key"), row);
		}
		for (ParameterKey<?> key : ParameterKeys.all()) {
			Map<String, Object> row = byKey.get(key.name());
			assertThat(row).as("persisted row for " + key.name()).isNotNull();
			assertThat(row.get("kind")).as(key.name() + " kind").isEqualTo(key.kind());
			assertThat(row.get("value_type")).as(key.name() + " value_type").isEqualTo(expectedType(key));
			assertThat(row.get("unit")).as(key.name() + " unit").isEqualTo(key.unit());
			assertThat(row.get("min_value")).as(key.name() + " min").isEqualTo(key.min());
			assertThat(row.get("max_value")).as(key.name() + " max").isEqualTo(key.max());
			assertThat(row.get("default_value")).as(key.name() + " default").isEqualTo(key.defaultValue() == null ? ""
					: key.defaultValue());
			assertThat(row.get("scope")).as(key.name() + " scope").isEqualTo(key.scope());
			assertThat(row.get("required")).as(key.name() + " required").isEqualTo(key.required());
			assertThat(row.get("owner_role")).as(key.name() + " owner").isEqualTo(key.ownerRole());
			assertThat(row.get("environments")).as(key.name() + " environments")
				.isEqualTo(String.join(",", key.environments()));
			assertThat(row.get("used_by")).as(key.name() + " used_by").isEqualTo(String.join("; ", key.usedBy()));
			assertThat(row.get("secret")).as(key.name() + " secret").isEqualTo(key.secret());
			assertThat(row.get("description")).as(key.name() + " description").isEqualTo(key.description());
		}

		// A fixture catalog with one changed default and no migration fails the comparison, naming key
		// and column.
		CatalogFileParser.Result drift = CatalogFileParser
			.parse(Path.of("src/test/resources/architecture/fixtures/parameter-checks/catalog/drift.csv"));
		CatalogRow changed = drift.rows()
			.stream()
			.filter(candidate -> candidate.key().equals("case.entry.dpd"))
			.findFirst()
			.orElseThrow();
		Map<String, Object> persistedEntry = byKey.get("case.entry.dpd");
		assertThat(persistedEntry.get("default_value")).isNotEqualTo(changed.defaultValue());
		assertThatThrownBy(() -> assertThat(persistedEntry.get("default_value"))
			.as("case.entry.dpd default_value").isEqualTo(changed.defaultValue()))
			.isInstanceOf(AssertionError.class)
			.hasMessageContaining("case.entry.dpd")
			.hasMessageContaining("default_value");
	}

	private static String expectedType(ParameterKey<?> key) {
		Class<?> type = key.type();
		if (type == Integer.class) {
			return "INTEGER";
		}
		if (type == java.math.BigDecimal.class) {
			return "DECIMAL";
		}
		if (type == Boolean.class) {
			return "BOOLEAN";
		}
		if (type == java.time.LocalDate.class) {
			return "DATE";
		}
		if (type == java.time.LocalTime.class) {
			return "TIME";
		}
		if (type == java.time.Duration.class) {
			return "DURATION";
		}
		return type == List.class ? "CODE_LIST" : "STRING";
	}

	private static List<Map<String, Object>> rows(String schema, String sql) throws SQLException {
		List<Map<String, Object>> rows = new ArrayList<>();
		try (Connection connection = connect();
				Statement statement = connection.createStatement();
				ResultSet results = statement.executeQuery(sql)) {
			int count = results.getMetaData().getColumnCount();
			while (results.next()) {
				Map<String, Object> row = new LinkedHashMap<>();
				for (int i = 1; i <= count; i++) {
					row.put(results.getMetaData().getColumnLabel(i).toLowerCase(), results.getObject(i));
				}
				rows.add(row);
			}
		}
		return rows;
	}

	/** A UUID column proves the seed identity is not a person: it is the synthetic seed value. */
	@Test
	void theSeedIdentityIsSynthetic() {
		assertThat(UUID.fromString(SEED_IDENTITY).version()).isEqualTo(0);
	}
}
