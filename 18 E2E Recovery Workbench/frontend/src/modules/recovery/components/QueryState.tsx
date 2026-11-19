import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/card";
import { ApiError } from "@/contexts/ApiClientContext";

interface QueryStateProps {
  isPending: boolean;
  error: unknown;
  onRetry: () => void;
  children: ReactNode;
}

/**
 * Loading, error, forbidden and signed-out states for one query (frontend-context §5). An error
 * shows the API's own message and the message ID as a reference, never a stack trace.
 */
export function QueryState({ isPending, error, onRetry, children }: QueryStateProps) {
  const { t, i18n } = useTranslation();

  if (isPending) {
    return (
      <div role="status" aria-live="polite" className="space-y-2">
        <span className="sr-only">{t("state.loading")}</span>
        <Skeleton className="h-5 w-2/3" />
        <Skeleton className="h-5 w-1/2" />
        <Skeleton className="h-5 w-3/5" />
      </div>
    );
  }

  if (error) {
    const apiError = error instanceof ApiError ? error : null;
    const forbidden = apiError?.status === 403;
    return (
      <div role="alert" className="rounded-md border border-border bg-error-bg p-4 text-error-fg">
        {forbidden && <p className="font-semibold">{t("state.forbiddenTitle")}</p>}
        <p>{apiError ? apiError.text(i18n.language) : String(error)}</p>
        {apiError?.messageId && <p className="mt-1 text-xs">{t("state.errorRef", { id: apiError.messageId })}</p>}
        {!forbidden && (
          <Button variant="secondary" className="mt-3" onClick={onRetry}>
            {t("state.retry")}
          </Button>
        )}
      </div>
    );
  }

  return <>{children}</>;
}
