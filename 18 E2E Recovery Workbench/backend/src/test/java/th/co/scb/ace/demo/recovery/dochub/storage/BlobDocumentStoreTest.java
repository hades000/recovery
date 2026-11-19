package th.co.scb.ace.demo.recovery.dochub.storage;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Optional;
import java.util.UUID;

import com.azure.core.http.HttpHeaders;
import com.azure.core.http.HttpResponse;
import com.azure.core.util.BinaryData;
import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.models.BlobErrorCode;
import com.azure.storage.blob.models.BlobStorageException;
import com.azure.storage.blob.options.BlobParallelUploadOptions;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import th.co.scb.ace.demo.recovery.dochub.api.DocumentStore;

/**
 * RWB-TE-001 SPEC-024: {@code BlobDocumentStore} keeps the standard and legal write paths, the
 * write-once refusal, the read paths and the client configuration.
 */
class BlobDocumentStoreTest {

	private static final UUID DOCUMENT_ID = UUID.fromString("00000000-0000-0000-0000-000000000010");

	private static final byte[] CONTENT = "synthetic document content".getBytes(StandardCharsets.UTF_8);

	private static final BlobDocumentStore.BlobProperties PROPERTIES = new BlobDocumentStore.BlobProperties(null,
			null, "rwb-documents", "rwb-documents-legal");

	private final BlobServiceClient service = mock(BlobServiceClient.class);

	private final BlobContainerClient documents = mock(BlobContainerClient.class);

	private final BlobContainerClient legal = mock(BlobContainerClient.class);

	private final BlobClient blob = mock(BlobClient.class);

	@Test
	void standardPutUploadsWithoutAConditionAndReturnsDigestAndSize() {
		BlobDocumentStore store = store();
		when(documents.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);

		DocumentStore.StoredDocument stored = store.put(DOCUMENT_ID, false, "application/pdf", CONTENT);

		BlobParallelUploadOptions options = capturedOptions();
		assertThat(options.getHeaders().getContentType()).isEqualTo("application/pdf");
		assertThat(options.getRequestConditions()).isNull();
		assertThat(stored.documentId()).isEqualTo(DOCUMENT_ID);
		assertThat(stored.container()).isEqualTo("rwb-documents");
		assertThat(stored.blobName()).isEqualTo(DOCUMENT_ID.toString());
		assertThat(stored.sha256()).isEqualTo(sha256(CONTENT));
		assertThat(stored.size()).isEqualTo(CONTENT.length);
	}

	@Test
	void legalPutUsesIfNoneMatchStar() {
		BlobDocumentStore store = store();
		when(legal.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);

		store.put(DOCUMENT_ID, true, "application/pdf", CONTENT);

		BlobParallelUploadOptions options = capturedOptions();
		assertThat(options.getRequestConditions()).isNotNull();
		assertThat(options.getRequestConditions().getIfNoneMatch()).isEqualTo("*");
	}

	@Test
	void legalOverwriteIsRefused() {
		BlobDocumentStore store = store();
		when(legal.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);
		BlobStorageException failure = storageError(BlobErrorCode.BLOB_ALREADY_EXISTS, 409);
		when(blob.uploadWithResponse(any(BlobParallelUploadOptions.class), isNull(), isNull())).thenThrow(failure);

		assertThatThrownBy(() -> store.put(DOCUMENT_ID, true, "application/pdf", CONTENT))
			.isInstanceOf(DocumentStore.DocumentImmutableException.class);
	}

	@Test
	void otherStorageErrorOnPutIsRethrown() {
		BlobDocumentStore store = store();
		when(documents.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);
		BlobStorageException failure = storageError(BlobErrorCode.CONTAINER_NOT_FOUND, 404);
		when(blob.uploadWithResponse(any(BlobParallelUploadOptions.class), isNull(), isNull())).thenThrow(failure);

		assertThatThrownBy(() -> store.put(DOCUMENT_ID, false, "application/pdf", CONTENT)).isSameAs(failure);
	}

	@Test
	void containerIsCreatedOncePerContainer() {
		BlobDocumentStore store = store();
		when(documents.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);

		store.put(DOCUMENT_ID, false, "application/pdf", CONTENT);
		store.put(DOCUMENT_ID, false, "application/pdf", CONTENT);

		verify(documents, times(1)).createIfNotExists();
	}

	@Test
	void getReturnsTheStoredBytes() {
		BlobDocumentStore store = store();
		when(documents.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);
		when(blob.downloadContent()).thenReturn(BinaryData.fromBytes(CONTENT));

		Optional<byte[]> content = store.get(DOCUMENT_ID, false);

		assertThat(content).contains(CONTENT);
	}

	@Test
	void getReturnsEmptyWhenTheBlobIsAbsent() {
		BlobDocumentStore store = store();
		when(legal.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);
		BlobStorageException failure = storageError(BlobErrorCode.BLOB_NOT_FOUND, 404);
		when(blob.downloadContent()).thenThrow(failure);

		Optional<byte[]> content = store.get(DOCUMENT_ID, true);

		assertThat(content).isEmpty();
	}

	@Test
	void otherStorageErrorOnGetIsRethrown() {
		BlobDocumentStore store = store();
		when(documents.getBlobClient(DOCUMENT_ID.toString())).thenReturn(blob);
		BlobStorageException failure = storageError(BlobErrorCode.CONTAINER_NOT_FOUND, 404);
		when(blob.downloadContent()).thenThrow(failure);

		assertThatThrownBy(() -> store.get(DOCUMENT_ID, false)).isSameAs(failure);
	}

	@Test
	void configUsesTheConnectionString() {
		BlobServiceClient client = new BlobDocumentStore.Config()
			.blobServiceClient(new BlobDocumentStore.BlobProperties(
					"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
							+ "AccountKey=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=;"
							+ "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;",
					null, "rwb-documents", "rwb-documents-legal"));

		assertThat(client.getAccountUrl()).contains("127.0.0.1:10000");
	}

	@Test
	void configUsesTheEndpointWithACredential() {
		BlobServiceClient client = new BlobDocumentStore.Config()
			.blobServiceClient(new BlobDocumentStore.BlobProperties(null, "https://account.example.invalid",
					"rwb-documents", "rwb-documents-legal"));

		assertThat(client.getAccountUrl()).contains("account.example.invalid");
	}

	@Test
	void configWithoutConnectionStringOrEndpointFails() {
		BlobDocumentStore.Config config = new BlobDocumentStore.Config();
		BlobDocumentStore.BlobProperties properties = new BlobDocumentStore.BlobProperties(null, null,
				"rwb-documents", "rwb-documents-legal");

		assertThatThrownBy(() -> config.blobServiceClient(properties)).isInstanceOf(IllegalStateException.class)
			.hasMessageContaining("rwb.blob.connection-string");
	}

	private BlobDocumentStore store() {
		when(service.getBlobContainerClient("rwb-documents")).thenReturn(documents);
		when(service.getBlobContainerClient("rwb-documents-legal")).thenReturn(legal);
		when(documents.getBlobContainerName()).thenReturn("rwb-documents");
		when(legal.getBlobContainerName()).thenReturn("rwb-documents-legal");
		return new BlobDocumentStore(service, PROPERTIES);
	}

	private BlobParallelUploadOptions capturedOptions() {
		ArgumentCaptor<BlobParallelUploadOptions> captor = ArgumentCaptor.forClass(BlobParallelUploadOptions.class);
		verify(blob).uploadWithResponse(captor.capture(), isNull(), isNull());
		return captor.getValue();
	}

	private static BlobStorageException storageError(BlobErrorCode code, int status) {
		HttpResponse response = mock(HttpResponse.class);
		when(response.getHeaders()).thenReturn(new HttpHeaders().set("x-ms-error-code", code.toString()));
		when(response.getStatusCode()).thenReturn(status);
		return new BlobStorageException("synthetic storage error", response, null);
	}

	private static String sha256(byte[] content) {
		try {
			return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(content));
		}
		catch (NoSuchAlgorithmException ex) {
			throw new IllegalStateException(ex);
		}
	}
}
