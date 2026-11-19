package th.co.scb.ace.demo.recovery.casewf.migration;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * SPEC-RWB-E1-044-002 (CLAR-009): registers the migration properties record with no condition, so
 * {@code rwb.schema} is pinned on every start, including when {@code rwb.flyway.enabled=false}.
 */
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(RecoveryMigrationProperties.class)
class MigrationPropertiesConfig {

}
