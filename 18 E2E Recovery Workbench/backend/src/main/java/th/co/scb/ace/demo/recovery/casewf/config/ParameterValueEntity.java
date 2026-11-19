package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * One row of {@code parameter_value} (Physical Schema v6, columns 1-19, plus the three columns this
 * story adds). The schema comes from {@code hibernate.default_schema}; no schema literal appears
 * here. The lifecycle column is {@code status}; {@code is_active} is never changed and never read.
 */
@Entity
@Table(name = "parameter_value")
class ParameterValueEntity {

	@Id
	UUID id;

	@Column(name = "param_key", nullable = false)
	String paramKey;

	@Column(nullable = false)
	String environment;

	@Column(name = "param_value", nullable = false)
	String paramValue;

	@Column(name = "product_group")
	String productGroup;

	@Column(name = "version_no", nullable = false)
	int versionNo;

	@Column(name = "valid_from", nullable = false)
	LocalDate validFrom;

	@Column(name = "valid_to")
	LocalDate validTo;

	@Column(nullable = false)
	String status;

	@Column(name = "author_user_id", nullable = false)
	UUID authorUserId;

	@Column(name = "approver_user_id")
	UUID approverUserId;

	@Column(name = "approved_at")
	Instant approvedAt;

	@Column(name = "is_active", nullable = false)
	boolean active = true;

	@Column
	String state;

	@Column(nullable = false)
	int version = 1;

	@Column(name = "created_at", nullable = false)
	Instant createdAt = Instant.now();

	@Column(name = "created_by")
	UUID createdBy;

	@Column(name = "updated_at", nullable = false)
	Instant updatedAt = Instant.now();

	@Column(name = "updated_by")
	UUID updatedBy;

	@Column(name = "load_id")
	UUID loadId;

	@Column(name = "content_hash")
	String contentHash;

	@Column(name = "rollback_reason")
	String rollbackReason;
}