package th.co.scb.ace.boundaryfixture.passing.recovery.integration.adapter;

import com.azure.storage.blob.BlobClient;

import java.net.http.HttpClient;

/** RWB-TE-001 fixture AC5: client libraries in the module's own client package are allowed. */
class PartnerHttpAdapter {

	private HttpClient http;

	private BlobClient blob;
}