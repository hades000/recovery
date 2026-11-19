package th.co.scb.ace.demo.recovery.integration.flags;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;

@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(RecoveryFlagProperties.class)
class PlatformConfig {

	@Bean
	RecoveryFlags recoveryFlags(RecoveryFlagProperties properties) {
		return new RecoveryFlags(properties.temporal(), properties.drools());
	}
}
