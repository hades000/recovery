import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect, useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import type { User } from "oidc-client-ts";
import { BrowserRouter, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth, userManager } from "@/auth/auth";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ApiClientProvider, ApiError } from "@/contexts/ApiClientContext";
import { AceLayout } from "@/layout/AceLayout";
import { RecoveryRoutes } from "@/modules/recovery/routes";

const queryClient = new QueryClient({
  defaultOptions: {
    // No retry on sign-in, permission or scope errors: retrying cannot change the answer.
    queries: { retry: (count, error) => count < 2 && !(error instanceof ApiError && [401, 403, 404].includes(error.status)) },
  },
});

// React StrictMode runs the callback effect twice in development. oidc-client-ts removes the stored
// sign-in state on the first call, so a second call failed and its catch sent the user to /recovery,
// racing the first call's navigation to returnTo (REVIEW-001 M11). The callback runs once per page
// load: the sign-in redirect leaves the app, so this module is fresh on every return.
let signInCallback: Promise<User> | undefined;

export function AuthCallback() {
  const navigate = useNavigate();
  useEffect(() => {
    signInCallback ??= userManager.signinRedirectCallback();
    signInCallback
      .then((user) => navigate((user.state as { returnTo?: string } | undefined)?.returnTo ?? "/recovery", { replace: true }))
      .catch(() => navigate("/recovery", { replace: true }));
  }, [navigate]);
  return null;
}

function RequireSignIn({ children }: { children: ReactNode }) {
  const { user, ready, signIn } = useAuth();
  const { t } = useTranslation();
  if (!ready) return null;
  if (!user) {
    return (
      <Card className="max-w-md space-y-3">
        <h1 className="text-lg font-semibold">{t("state.signInTitle")}</h1>
        <Button onClick={() => void signIn()}>{t("state.signIn")}</Button>
      </Card>
    );
  }
  return <>{children}</>;
}

function Shell() {
  const { getAccessToken } = useAuth();
  const [client] = useState(() => queryClient);
  return (
    <ApiClientProvider getAccessToken={getAccessToken}>
      <QueryClientProvider client={client}>
        <AceLayout>
          <Routes>
            <Route path="/" element={<Navigate to="/recovery" replace />} />
            <Route path="/auth/callback" element={<AuthCallback />} />
            <Route
              path="/recovery/*"
              element={
                <RequireSignIn>
                  <RecoveryRoutes />
                </RequireSignIn>
              }
            />
          </Routes>
        </AceLayout>
      </QueryClientProvider>
    </ApiClientProvider>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Shell />
      </AuthProvider>
    </BrowserRouter>
  );
}
