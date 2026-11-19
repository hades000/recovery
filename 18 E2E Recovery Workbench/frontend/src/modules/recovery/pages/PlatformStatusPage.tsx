import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";
import { Badge, Card, CardTitle } from "@/components/ui/card";
import { usePlatformInfo, useStartSmokeWorkflow, useTemporalHealth } from "@/modules/recovery/api/platform";
import { QueryState } from "@/modules/recovery/components/QueryState";

/** Platform screen group (E1-070/071): service, flags, the ADR-010 boundary and Temporal health. */
export function PlatformStatusPage() {
  const { t } = useTranslation();
  const info = usePlatformInfo();
  const temporalOn = info.data?.flags.temporal ?? false;
  const temporal = useTemporalHealth(temporalOn);
  const smoke = useStartSmokeWorkflow();

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-semibold">{t("platform.title")}</h1>
        <Button variant="secondary" onClick={() => void info.refetch()}>
          {t("platform.refresh")}
        </Button>
      </div>

      <QueryState isPending={info.isPending} error={info.error} onRetry={() => void info.refetch()}>
        {info.data && (
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardTitle>{t("platform.service")}</CardTitle>
              <dl className="grid grid-cols-2 gap-y-2 text-sm">
                <dt className="text-muted-foreground">{t("platform.service")}</dt>
                <dd>{info.data.service}</dd>
                <dt className="text-muted-foreground">{t("platform.environment")}</dt>
                <dd>{info.data.environment}</dd>
                <dt className="text-muted-foreground">{t("platform.flags")}</dt>
                <dd className="flex flex-wrap gap-2">
                  <Badge tone={info.data.flags.temporal ? "ok" : "neutral"}>
                    rwb.p3.temporal: {info.data.flags.temporal ? t("platform.flagOn") : t("platform.flagOff")}
                  </Badge>
                  <Badge tone={info.data.flags.drools ? "ok" : "neutral"}>
                    rwb.p3.drools: {info.data.flags.drools ? t("platform.flagOn") : t("platform.flagOff")}
                  </Badge>
                </dd>
              </dl>
            </Card>

            <Card>
              <CardTitle>{t("platform.database")}</CardTitle>
              <dl className="grid grid-cols-2 gap-y-2 text-sm">
                <dt className="text-muted-foreground">{t("platform.schema")}</dt>
                <dd>{info.data.database.schema}</dd>
                <dt className="text-muted-foreground">{t("platform.recoveryTables")}</dt>
                <dd>{info.data.database.recoveryTables}</dd>
                <dt className="text-muted-foreground">{t("platform.aceViews")}</dt>
                <dd>{info.data.database.aceViews}</dd>
                <dt className="text-muted-foreground">{t("platform.publicTables")}</dt>
                <dd className="flex items-center gap-2">
                  {info.data.database.visiblePublicTables}
                  <Badge tone={info.data.database.visiblePublicTables === 0 ? "ok" : "error"}>
                    {info.data.database.visiblePublicTables === 0 ? t("platform.boundaryOk") : t("platform.boundaryBroken")}
                  </Badge>
                </dd>
              </dl>
            </Card>
          </div>
        )}
      </QueryState>

      {info.data && (
        <Card>
          <CardTitle>{t("platform.temporal")}</CardTitle>
          {!temporalOn ? (
            <p className="text-sm text-muted-foreground">{t("platform.temporalOff")}</p>
          ) : (
            <QueryState isPending={temporal.isPending} error={temporal.error} onRetry={() => void temporal.refetch()}>
              {temporal.data && (
                <div className="space-y-4">
                  <dl className="grid grid-cols-2 gap-y-2 text-sm md:grid-cols-4">
                    <dt className="text-muted-foreground">{t("platform.namespace")}</dt>
                    <dd>{temporal.data.namespace}</dd>
                    <dt className="text-muted-foreground">{t("platform.state")}</dt>
                    <dd>{temporal.data.state}</dd>
                    <dt className="text-muted-foreground">{t("platform.retention")}</dt>
                    <dd>{t("platform.retentionDays", { count: temporal.data.retentionDays })}</dd>
                  </dl>
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b border-border">
                        <th scope="col" className="py-2">{t("platform.taskQueue")}</th>
                        <th scope="col" className="py-2">{t("platform.pollers")}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {temporal.data.taskQueues.map((q) => (
                        <tr key={q.name} className="border-b border-border last:border-0">
                          <td className="py-2 font-mono">{q.name}</td>
                          <td className="py-2">{q.workflowPollers}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </QueryState>
          )}
          {temporalOn && (
            <div className="mt-4 space-y-2">
              <Button onClick={() => smoke.mutate()} disabled={smoke.isPending}>
                {t("platform.startSmoke")}
              </Button>
              {smoke.data?.workflowId && (
                <p role="status" className="text-sm">
                  {t("platform.smokeStarted", { id: smoke.data.workflowId })}
                </p>
              )}
              {smoke.error && (
                <QueryState isPending={false} error={smoke.error} onRetry={() => smoke.mutate()}>
                  {null}
                </QueryState>
              )}
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
