package th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal;

import java.net.SocketTimeoutException;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

/** RWB-TE-001 fixture AC5: only java.net.URL matches the java.net.URL client-library entry. */
class UrlHelper {

	private URL url;

	private URI uri;

	private SocketTimeoutException timeout;

	String encoded(String text) {
		return URLEncoder.encode(text, StandardCharsets.UTF_8) + uri + url + timeout;
	}
}
