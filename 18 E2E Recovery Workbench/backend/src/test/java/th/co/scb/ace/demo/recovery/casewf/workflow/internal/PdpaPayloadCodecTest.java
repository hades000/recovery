package th.co.scb.ace.demo.recovery.casewf.workflow.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.security.SecureRandom;
import java.util.Base64;
import java.util.List;

import com.google.protobuf.ByteString;
import io.temporal.api.common.v1.Payload;
import io.temporal.payload.codec.PayloadCodecException;
import org.junit.jupiter.api.Test;

class PdpaPayloadCodecTest {

	static String newKey() {
		byte[] raw = new byte[32];
		new SecureRandom().nextBytes(raw);
		return Base64.getEncoder().encodeToString(raw);
	}

	private final String key = newKey();
	private final PdpaPayloadCodec codec = new PdpaPayloadCodec(key, "k1");

	private static Payload plain(String json) {
		return Payload.newBuilder().putMetadata("encoding", ByteString.copyFromUtf8("json/plain"))
				.setData(ByteString.copyFromUtf8(json)).build();
	}

	@Test
	void historyHoldsNoClearValue() {
		Payload original = plain("{\"customerName\":\"Synthetic Person\"}");

		Payload encoded = codec.encode(List.of(original)).getFirst();

		assertThat(encoded.getData().toStringUtf8()).doesNotContain("Synthetic Person");
		assertThat(encoded.getMetadataOrThrow("encoding").toStringUtf8()).isEqualTo("binary/encrypted");
		assertThat(encoded.getMetadataOrThrow("encryption-key-id").toStringUtf8()).isEqualTo("k1");
		assertThat(codec.decode(List.of(encoded))).containsExactly(original);
	}

	@Test
	void sameValueEncryptsDifferentlyEachTime() {
		Payload original = plain("\"x\"");
		assertThat(codec.encode(List.of(original)).getFirst().getData())
				.isNotEqualTo(codec.encode(List.of(original)).getFirst().getData());
	}

	@Test
	void unencryptedPayloadPassesThrough() {
		Payload original = plain("\"x\"");
		assertThat(codec.decode(List.of(original))).containsExactly(original);
	}

	@Test
	void unknownKeyIdIsRefused() {
		Payload encoded = new PdpaPayloadCodec(newKey(), "other").encode(List.of(plain("\"x\""))).getFirst();
		assertThatThrownBy(() -> codec.decode(List.of(encoded))).isInstanceOf(PayloadCodecException.class);
	}

	@Test
	void tamperedPayloadIsRefused() {
		Payload encoded = codec.encode(List.of(plain("\"x\""))).getFirst();
		byte[] data = encoded.getData().toByteArray();
		data[data.length - 1] ^= 1;
		Payload tampered = encoded.toBuilder().setData(ByteString.copyFrom(data)).build();
		assertThatThrownBy(() -> codec.decode(List.of(tampered))).isInstanceOf(PayloadCodecException.class);
	}

	@Test
	void sixteenAndTwentyFourByteKeysAreAccepted() {
		assertThatCode(() -> new PdpaPayloadCodec(Base64.getEncoder().encodeToString(new byte[16]), "k1"))
				.doesNotThrowAnyException();
		assertThatCode(() -> new PdpaPayloadCodec(Base64.getEncoder().encodeToString(new byte[24]), "k1"))
				.doesNotThrowAnyException();
	}

	@Test
	void missingOrBadKeyFailsAtStartup() {
		assertThatThrownBy(() -> new PdpaPayloadCodec("", "k1")).hasMessageContaining("codec-key is required");
		assertThatThrownBy(() -> new PdpaPayloadCodec(Base64.getEncoder().encodeToString(new byte[5]), "k1"))
				.hasMessageContaining("128, 192 or 256");
	}
}
