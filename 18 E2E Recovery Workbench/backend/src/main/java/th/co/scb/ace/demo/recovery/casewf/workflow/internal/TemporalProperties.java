package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import java.time.Duration;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * {@code rwb.temporal.*}, mirroring parameters {@code temporal.target}, {@code temporal.namespace}
 * and {@code temporal.taskqueue.platform}. {@code codecKey} is a base64 AES key from Key Vault (or
 * {@code .env} locally); it is never committed.
 */
@ConfigurationProperties(prefix = "rwb.temporal")
public record TemporalProperties(String target, String namespace, String codecKey, String codecKeyId, Duration rpcTimeout) {
}
