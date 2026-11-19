package th.co.scb.ace.demo.recovery.dochub.storage;

import java.io.ByteArrayInputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import com.azure.core.util.BinaryData;
import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import com.azure.storage.blob.models.BlobErrorCode;
import com.azure.storage.blob.models.BlobHttpHeaders;
import com.azure.storage.blob.models.BlobRequestConditions;
import com.azure.storage.blob.models.BlobStorageException;
import com.azure.storage.blob.options.BlobParallelUploadOptions;
import com.azure.identity.DefaultAzureCredentialBuilder;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

import th.co.scb.ace.demo.recovery.dochub.api.DocumentStore;

/**
 * {@link DocumentStore} on Azure Blob. Locally the client uses the Azurite connection string; in
 * SIT/UAT/PROD it uses the managed identity against {@code rwb.blob.endpoint}.
 *
 * <p>Write-once is enforced here with an {@code If-None-Match: *} upload, and in Azure by the
 * container's immutability policy. Azurite has no immutability policy, so locally only the
 * conditional upload protects legal documents.
 */
class BlobDocumentStore implements DocumentStore {

	private final BlobContainerClient documents;
	private final BlobContainerClient legal;
	private final java.util.Set<String> ensured = ConcurrentHashMap.newKeySet();

	BlobDocumentStore(BlobServiceClient service, BlobProperties properties) {
		this.documents = service.getBlobContainerClient(properties.documentContainer());
		this.legal = service.getBlobContainerClient(properties.legalContainer());
	}

	@Override
	public StoredDocument put(UUID documentId, boolean legalType, String contentType, byte[] content) {
		BlobContainerClient container = ensure(legalType ? legal : documents);
		String name = documentId.toString();
		BlobClient blob = container.getBlobClient(name);
		BlobParallelUploadOptions options = new BlobParallelUploadOptions(new ByteArrayInputStream(content))
				.setHeaders(new BlobHttpHeaders().setContentType(contentType));
		if (legalType) {
			options.setRequestConditions(new BlobRequestConditions().setIfNoneMatch("*"));
		}
		try {
			blob.uploadWithResponse(options, null, null);
		}
		catch (BlobStorageException ex) {
			if (legalType && BlobErrorCode.BLOB_ALREADY_EXISTS.equals(ex.getErrorCode())) {
				throw new DocumentImmutableException(documentId);
			}
			throw ex;
		}
		return new StoredDocument(documentId, container.getBlobContainerName(), name, sha256(content), content.length);
	}

	@Override
	public Optional<byte[]> get(UUID documentId, boolean legalType) {
		BlobClient blob = (legalType ? legal : documents).getBlobClient(documentId.toString());
		try {
			BinaryData data = blob.downloadContent();
			return Optional.of(data.toBytes());
		}
		catch (BlobStorageException ex) {
			if (BlobErrorCode.BLOB_NOT_FOUND.equals(ex.getErrorCode())) {
				return Optional.empty();
			}
			throw ex;
		}
	}

	/** Containers are created on first write, so the service starts while Blob storage is down. */
	private BlobContainerClient ensure(BlobContainerClient container) {
		if (ensured.add(container.getBlobContainerName())) {
			container.createIfNotExists();
		}
		return container;
	}

	private static String sha256(byte[] content) {
		try {
			return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(content));
		}
		catch (NoSuchAlgorithmException ex) {
			throw new IllegalStateException(ex);
		}
	}

	@ConfigurationProperties(prefix = "rwb.blob")
	record BlobProperties(String connectionString, String endpoint, String documentContainer, String legalContainer) {
	}

	@Configuration(proxyBeanMethods = false)
	@EnableConfigurationProperties(BlobProperties.class)
	static class Config {

		@Bean
		BlobServiceClient blobServiceClient(BlobProperties properties) {
			BlobServiceClientBuilder builder = new BlobServiceClientBuilder();
			if (StringUtils.hasText(properties.connectionString())) {
				return builder.connectionString(properties.connectionString()).buildClient();
			}
			if (!StringUtils.hasText(properties.endpoint())) {
				throw new IllegalStateException("Set rwb.blob.connection-string (local) or rwb.blob.endpoint (managed identity)");
			}
			return builder.endpoint(properties.endpoint()).credential(new DefaultAzureCredentialBuilder().build()).buildClient();
		}

		@Bean
		BlobDocumentStore documentStore(BlobServiceClient service, BlobProperties properties) {
			return new BlobDocumentStore(service, properties);
		}
	}
}
