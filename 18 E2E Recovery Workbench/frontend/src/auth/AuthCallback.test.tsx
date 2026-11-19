import { render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

// REVIEW-001 M11: under StrictMode the callback effect runs twice. oidc-client-ts consumes the stored
// state on the first call, so a second call rejects; the user must still land on returnTo.
const signinRedirectCallback = vi.hoisted(() => vi.fn());
vi.mock("@/auth/auth", () => ({
  userManager: { signinRedirectCallback },
  AuthProvider: ({ children }: { children: unknown }) => children,
  useAuth: () => ({ user: null, ready: true, signIn: vi.fn(), signOut: vi.fn(), getAccessToken: vi.fn() }),
}));

import { AuthCallback } from "@/App";

describe("AuthCallback", () => {
  it("completes the sign-in once and lands on returnTo under StrictMode", async () => {
    signinRedirectCallback
      .mockResolvedValueOnce({ state: { returnTo: "/recovery/platform" } })
      .mockRejectedValue(new Error("No matching state found in storage"));

    render(
      <StrictMode>
        <MemoryRouter initialEntries={["/auth/callback"]}>
          <Routes>
            <Route path="/auth/callback" element={<AuthCallback />} />
            <Route path="/recovery/platform" element={<p>platform</p>} />
            <Route path="/recovery" element={<p>overview</p>} />
          </Routes>
        </MemoryRouter>
      </StrictMode>,
    );

    expect(await screen.findByText("platform")).toBeInTheDocument();
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(screen.getByText("platform")).toBeInTheDocument();
    expect(signinRedirectCallback).toHaveBeenCalledTimes(1);
  });
});
