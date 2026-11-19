package th.co.scb.ace.demo.recovery.dochub.api;

import java.util.Optional;
import java.util.UUID;

/**
 * Binary store of the document hub (ADR-007). The {@code document} and {@code document_index} rows
 * stay the record; this holds only the bytes. Legal types go to the write-once container, so a
 * second write of the same legal document is refused.
 */
public interface DocumentStore {

	StoredDocument put(UUID documentId, boolean legal, String contentType, byte[] content);

	Optional<byte[]> get(UUID documentId, boolean legal);

	record StoredDocument(UUID documentId, String container, String blobName, String sha256, long size) {
	}

	/** A legal document already exists and cannot be overwritten. */
	class DocumentImmutableException extends RuntimeException {

		public DocumentImmutableException(UUID documentId) {
			super("Legal document is write-once: " + documentId);
		}
	}
}
