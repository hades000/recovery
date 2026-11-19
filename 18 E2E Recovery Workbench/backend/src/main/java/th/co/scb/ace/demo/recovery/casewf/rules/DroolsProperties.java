package th.co.scb.ace.demo.recovery.casewf.rules;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/** {@code rwb.drools.*}. The KieBase cache size mirrors parameter {@code drools.kiebase.cache.max}. */
@ConfigurationProperties(prefix = "rwb.drools")
record DroolsProperties(int kiebaseCacheMax) {

	@Configuration(proxyBeanMethods = false)
	@EnableConfigurationProperties(DroolsProperties.class)
	static class Registration {
	}
}
