package th.co.scb.ace.boundaryfixture.bnd5.vendor;

/** RWB-TE-001 fixture AC5: vendor client outside the recovery root, matched as a client library. */
public final class VendorClient {

	private VendorClient() {
	}

	/** Nested session type; the client-library entry matches on the '$' boundary. */
	public static final class Session {
	}
}