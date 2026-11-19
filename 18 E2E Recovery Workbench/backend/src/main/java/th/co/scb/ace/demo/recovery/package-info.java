/**
 * Recovery Workbench: the recovery module of ACE (ADR-001, ADR-002).
 *
 * <p>One Spring Modulith application module. Design modules are nested application modules, each
 * with an {@code api} package (its published interface) and an {@code internal} package that no
 * other module may use (BS-1.1, BS-1.2). Source data is read only through {@code recovery.v_ace_*}
 * views (ADR-010, BND-6).
 */
@org.springframework.modulith.ApplicationModule(displayName = "Recovery")
package th.co.scb.ace.demo.recovery;
