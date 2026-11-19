import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useApiClient } from "@/contexts/ApiClientContext";

// Operational platform endpoints. /admin/workflows/smoke is in API Specification v4 and uses the
// generated types; /platform/info and /admin/temporal/health are local operational endpoints
// (backend-context §3, §7) and are typed here until the specification carries them.

export interface PlatformInfo {
  service: string;
  environment: string;
  flags: { temporal: boolean; drools: boolean };
  database: { schema: string; recoveryTables: number; aceViews: number; visiblePublicTables: number };
}

export interface TemporalHealth {
  target: string;
  namespace: string;
  state: string;
  retentionDays: number;
  taskQueues: { name: string; workflowPollers: number }[];
}

export const platformKeys = {
  info: ["recovery", "platform", "info"] as const,
  temporal: ["recovery", "platform", "temporal-health"] as const,
};

export function usePlatformInfo() {
  const { getJson } = useApiClient();
  return useQuery({ queryKey: platformKeys.info, queryFn: () => getJson<PlatformInfo>("/platform/info") });
}

export function useTemporalHealth(enabled: boolean) {
  const { getJson } = useApiClient();
  return useQuery({
    queryKey: platformKeys.temporal,
    queryFn: () => getJson<TemporalHealth>("/admin/temporal/health"),
    enabled,
  });
}

export function useStartSmokeWorkflow() {
  const { client } = useApiClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data } = await client.POST("/admin/workflows/smoke");
      return data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: platformKeys.temporal }),
  });
}
