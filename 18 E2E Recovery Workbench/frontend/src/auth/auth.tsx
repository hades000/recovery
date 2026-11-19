import { UserManager, WebStorageStateStore, type User } from "oidc-client-ts";
import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

// Sign-in for the local shell. In ACE the shell signs in to Entra ID with MFA and the recovery
// module never touches tokens: it calls the API through ApiClientContext. Locally the authority is
// the mock OIDC server (infra/mock-oidc), which shows a form to pick a user and its role claims.

const authority = import.meta.env.VITE_OIDC_AUTHORITY ?? "http://localhost:8090/entra";
const clientId = import.meta.env.VITE_OIDC_CLIENT_ID ?? "rwb-frontend";

export const userManager = new UserManager({
  authority,
  client_id: clientId,
  redirect_uri: `${window.location.origin}/auth/callback`,
  post_logout_redirect_uri: window.location.origin,
  response_type: "code",
  scope: "openid profile api://rwb-recovery/.default",
  userStore: new WebStorageStateStore({ store: window.sessionStorage }),
  automaticSilentRenew: false,
});

interface AuthState {
  user: User | null;
  ready: boolean;
  signIn: (returnTo?: string) => Promise<void>;
  signOut: () => Promise<void>;
  getAccessToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    userManager.getUser().then((u) => {
      setUser(u && !u.expired ? u : null);
      setReady(true);
    });
    const onLoaded = (u: User) => setUser(u);
    const onUnloaded = () => setUser(null);
    userManager.events.addUserLoaded(onLoaded);
    userManager.events.addUserUnloaded(onUnloaded);
    return () => {
      userManager.events.removeUserLoaded(onLoaded);
      userManager.events.removeUserUnloaded(onUnloaded);
    };
  }, []);

  const signIn = useCallback(async (returnTo?: string) => {
    await userManager.signinRedirect({ state: { returnTo: returnTo ?? window.location.pathname } });
  }, []);

  const signOut = useCallback(async () => {
    await userManager.removeUser();
    setUser(null);
  }, []);

  const getAccessToken = useCallback(async () => {
    const u = await userManager.getUser();
    return u && !u.expired ? u.access_token : null;
  }, []);

  const value = useMemo(() => ({ user, ready, signIn, signOut, getAccessToken }), [user, ready, signIn, signOut, getAccessToken]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
