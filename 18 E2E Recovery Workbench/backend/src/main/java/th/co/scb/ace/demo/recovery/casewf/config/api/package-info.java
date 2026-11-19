/**
 * Published interface of the configuration service (RWB-E1-042 SPEC-026, TE1S SPEC-004 (d)). P3
 * callers read parameters through {@link th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService};
 * every module outside P3 reads them through
 * {@link th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader} (D-RUN-19).
 */
@org.springframework.modulith.NamedInterface(name = "config.api", propagate = false)
package th.co.scb.ace.demo.recovery.casewf.config.api;