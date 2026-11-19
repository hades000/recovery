import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render } from "@testing-library/react";
import type { ReactElement } from "react";
import { MemoryRouter } from "react-router-dom";
import { ApiClientProvider } from "@/contexts/ApiClientContext";

type Handler = (request: Request) => Response | Promise<Response>;

/** Renders a screen with a fake API: each call goes to `handler` instead of the network. */
export function renderWithApi(ui: ReactElement, handler: Handler, route = "/") {
  const fetchImpl = (async (input: RequestInfo | URL, init?: RequestInit) =>
    handler(new Request(input, init))) as typeof fetch;
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <ApiClientProvider getAccessToken={async () => "test-token"} fetchImpl={fetchImpl}>
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>
      </QueryClientProvider>
    </ApiClientProvider>,
  );
}

export function json(body: unknown, status = 200, contentType = "application/json"): Response {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": contentType } });
}
