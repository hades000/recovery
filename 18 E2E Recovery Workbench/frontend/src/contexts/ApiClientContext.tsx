import createClient, { type Client } from "openapi-fetch";
import { createContext, useContext, useMemo, type ReactNode } from "react";
import type { paths } from "@/api/schema";

// The only way a recovery screen calls the API (frontend-context §6): no direct fetch in a
// component. Types are generated from API Specification v4 (npm run api:generate).

export const API_BASE = "/api/recovery/v1";

/** API Specification v4 Problem, normalised for screens: message in the user's language. */
export class ApiError extends Error {
  readonly status: number;
  readonly messageId: string | null;
  readonly messageTh: string | null;
  readonly traceId: string | null;

  constructor(status: number, body: Partial<Problem> | null) {
    super(body?.detail ?? `HTTP ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.messageId = body?.messageCode ?? null;
    this.messageTh = body?.messageTh ?? null;
    this.traceId = body?.traceId ?? null;
  }

  /** Text for the user: Thai when the UI is Thai and the API sent Thai, otherwise English. */
  text(language: string): string {
    return language.startsWith("th") && this.messageTh ? this.messageTh : this.message;
  }
}

interface Problem {
  type: string;
  title: string;
  status: number;
  detail: string;
  messageCode: string;
  messageTh: string;
  field: string;
  traceId: string;
}

export interface ApiClient {
  /** Typed client for every path in API Specification v4. */
  client: Client<paths>;
  /** Operational endpoints that are not yet in the specification (for example /admin/temporal/health). */
  getJson: <T>(path: string) => Promise<T>;
}

const ApiClientContext = createContext<ApiClient | null>(null);

export interface ApiClientProviderProps {
  getAccessToken: () => Promise<string | null>;
  fetchImpl?: typeof fetch;
  children: ReactNode;
}

export function ApiClientProvider({ getAccessToken, fetchImpl, children }: ApiClientProviderProps) {
  const value = useMemo<ApiClient>(() => {
    const doFetch: typeof fetch = async (input, init) => {
      const request = new Request(input, init);
      const token = await getAccessToken();
      if (token) request.headers.set("Authorization", `Bearer ${token}`);
      request.headers.set("X-Correlation-Id", crypto.randomUUID());
      return (fetchImpl ?? fetch)(request);
    };

    // Absolute base from the page origin: the API is served from the same origin as the shell.
    const client = createClient<paths>({ baseUrl: window.location.origin + API_BASE, fetch: doFetch });
    client.use({
      async onResponse({ response }) {
        if (!response.ok) throw await toApiError(response);
        return response;
      },
    });

    const getJson = async <T,>(path: string): Promise<T> => {
      const response = await doFetch(new Request(new URL(API_BASE + path, window.location.origin)));
      if (!response.ok) throw await toApiError(response);
      return (await response.json()) as T;
    };

    return { client, getJson };
  }, [getAccessToken, fetchImpl]);

  return <ApiClientContext.Provider value={value}>{children}</ApiClientContext.Provider>;
}

async function toApiError(response: Response): Promise<ApiError> {
  let body: Partial<Problem> | null = null;
  try {
    body = (await response.clone().json()) as Partial<Problem>;
  } catch {
    body = null;
  }
  return new ApiError(response.status, body);
}

export function useApiClient(): ApiClient {
  const ctx = useContext(ApiClientContext);
  if (!ctx) throw new Error("useApiClient must be used inside ApiClientProvider");
  return ctx;
}
