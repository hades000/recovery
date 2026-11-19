package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import java.nio.ByteBuffer;
import java.security.GeneralSecurityException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.List;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import com.google.protobuf.ByteString;
import com.google.protobuf.InvalidProtocolBufferException;
import io.temporal.api.common.v1.Payload;
import io.temporal.payload.codec.PayloadCodec;
import io.temporal.payload.codec.PayloadCodecException;

/**
 * Encrypts every Temporal payload with AES-GCM so workflow history holds no clear personal data
 * (ADR-011, BS-4.6). The key comes from Key Vault; the key ID travels in the payload metadata so a
 * rotated key can still decode old history. RW-SECADM decodes through the codec server on a
 * break-glass session only.
 */
final class PdpaPayloadCodec implements PayloadCodec {

	static final String METADATA_ENCODING_KEY = "encoding";
	static final ByteString ENCODING = ByteString.copyFromUtf8("binary/encrypted");
	static final String METADATA_KEY_ID = "encryption-key-id";
	private static final int IV_BYTES = 12;
	private static final int TAG_BITS = 128;

	private final SecretKey key;
	private final String keyId;
	private final SecureRandom random = new SecureRandom();

	PdpaPayloadCodec(String base64Key, String keyId) {
		if (base64Key == null || base64Key.isBlank()) {
			throw new IllegalStateException("rwb.temporal.codec-key is required when rwb.p3.temporal is on");
		}
		byte[] raw = Base64.getDecoder().decode(base64Key);
		if (raw.length != 16 && raw.length != 24 && raw.length != 32) {
			throw new IllegalStateException("rwb.temporal.codec-key must be a base64 AES key of 128, 192 or 256 bits");
		}
		this.key = new SecretKeySpec(raw, "AES");
		this.keyId = keyId;
	}

	@Override
	public List<Payload> encode(List<Payload> payloads) {
		return payloads.stream().map(this::encrypt).toList();
	}

	@Override
	public List<Payload> decode(List<Payload> payloads) {
		return payloads.stream().map(this::decrypt).toList();
	}

	private Payload encrypt(Payload payload) {
		try {
			byte[] iv = new byte[IV_BYTES];
			random.nextBytes(iv);
			Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
			cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(TAG_BITS, iv));
			byte[] sealed = cipher.doFinal(payload.toByteArray());
			byte[] out = ByteBuffer.allocate(iv.length + sealed.length).put(iv).put(sealed).array();
			return Payload.newBuilder()
					.putMetadata(METADATA_ENCODING_KEY, ENCODING)
					.putMetadata(METADATA_KEY_ID, ByteString.copyFromUtf8(keyId))
					.setData(ByteString.copyFrom(out))
					.build();
		}
		catch (GeneralSecurityException ex) {
			throw new PayloadCodecException(ex);
		}
	}

	private Payload decrypt(Payload payload) {
		if (!ENCODING.equals(payload.getMetadataOrDefault(METADATA_ENCODING_KEY, ByteString.EMPTY))) {
			return payload;
		}
		String payloadKeyId = payload.getMetadataOrDefault(METADATA_KEY_ID, ByteString.EMPTY).toStringUtf8();
		if (!keyId.equals(payloadKeyId)) {
			throw new PayloadCodecException("Unknown payload key ID: " + payloadKeyId, null);
		}
		try {
			byte[] data = payload.getData().toByteArray();
			Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
			cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(TAG_BITS, data, 0, IV_BYTES));
			byte[] plain = cipher.doFinal(data, IV_BYTES, data.length - IV_BYTES);
			return Payload.parseFrom(plain);
		}
		catch (GeneralSecurityException | InvalidProtocolBufferException ex) {
			throw new PayloadCodecException(ex);
		}
	}
}
