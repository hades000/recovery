package th.co.scb.ace.demo.recovery.access.internal;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.access.api.CapabilityCheck;

/**
 * Interim {@link CapabilityCheck} over the "Rules and parameters" column of Users, Roles and
 * Permissions v4 (SPEC-RWB-E1-042-020). Registered as bean {@code capabilityCheck}, the name the
 * method check resolves; RWB-E1-037 replaces this implementation and deletes the grants file, keeping
 * that bean name. The grants are data, never code: a role absent from the file holds no right.
 */
@Component("capabilityCheck")
class InterimCapabilityCheck implements CapabilityCheck {

	private final Map<String, String> grants;

	@org.springframework.beans.factory.annotation.Autowired
	InterimCapabilityCheck(@Value("classpath:access/interim-capability-grants.csv") Resource resource) {
		this(read(resource));
	}

	InterimCapabilityCheck(Map<String, String> grants) {
		this.grants = Map.copyOf(grants);
	}

	@Override
	public boolean has(Authentication authentication, String area, String right) {
		if (authentication == null || area == null || right == null || right.isEmpty()) {
			return false;
		}
		for (GrantedAuthority authority : authentication.getAuthorities()) {
			String role = role(authority.getAuthority());
			String rights = grants.get(key(role, area));
			if (rights != null && rights.indexOf(right.charAt(0)) >= 0) {
				return true;
			}
		}
		return false;
	}

	@Override
	public boolean require(Authentication authentication, String area, String right, String action) {
		if (has(authentication, area, right)) {
			return true;
		}
		throw new ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null);
	}

	static Map<String, String> read(Resource resource) {
		try (InputStream in = resource.getInputStream()) {
			return read(new String(in.readAllBytes(), StandardCharsets.UTF_8));
		}
		catch (IOException ex) {
			throw new UncheckedIOException("cannot read " + resource, ex);
		}
	}

	static Map<String, String> read(String text) {
		Map<String, String> grants = new LinkedHashMap<>();
		for (String line : text.replace("\r\n", "\n").split("\n")) {
			if (line.isBlank() || line.startsWith("role,")) {
				continue;
			}
			String[] cells = line.split(",", -1);
			if (cells.length < 3) {
				throw new IllegalStateException("grants row needs three columns: " + line);
			}
			grants.put(key(cells[0].trim(), cells[1].trim()), cells[2].trim());
		}
		return grants;
	}

	private static String key(String role, String area) {
		return role + "|" + area;
	}

	private static String role(String authority) {
		String upper = authority.toUpperCase(Locale.ROOT);
		return upper.startsWith("ROLE_") ? authority.substring("ROLE_".length()) : authority;
	}
}
