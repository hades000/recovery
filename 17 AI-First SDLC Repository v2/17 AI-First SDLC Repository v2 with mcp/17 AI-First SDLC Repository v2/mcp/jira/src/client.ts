import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Optional per-server .env (mcp/jira/.env); variables already set by the MCP client take precedence.
const envFile = resolve(dirname(fileURLToPath(import.meta.url)), "..", ".env");
if (existsSync(envFile)) process.loadEnvFile(envFile);

export interface JiraConfig {
  baseUrl: string;
  isCloud: boolean;
  authHeader: string;
}

export function loadConfig(): JiraConfig {
  const url = process.env.JIRA_URL?.trim();
  if (!url) throw new Error("JIRA_URL is not set (e.g. https://your-company.atlassian.net or https://jira.your-company.com)");
  const baseUrl = url.replace(/\/+$/, "");

  const email = process.env.JIRA_EMAIL?.trim();
  const apiToken = process.env.JIRA_API_TOKEN?.trim();
  const pat = process.env.JIRA_PAT?.trim();

  let authHeader: string;
  if (email && apiToken) {
    authHeader = "Basic " + Buffer.from(`${email}:${apiToken}`).toString("base64");
  } else if (pat) {
    authHeader = `Bearer ${pat}`;
  } else {
    throw new Error("Set JIRA_EMAIL + JIRA_API_TOKEN (Jira Cloud) or JIRA_PAT (Jira Server/Data Center)");
  }

  const deployment = process.env.JIRA_DEPLOYMENT?.trim().toLowerCase();
  const isCloud = deployment ? deployment === "cloud" : new URL(baseUrl).hostname.endsWith(".atlassian.net");

  return { baseUrl, isCloud, authHeader };
}

type Query = Record<string, string | number | boolean | undefined>;

export class JiraClient {
  constructor(readonly config: JiraConfig) {}

  async request<T = any>(method: string, path: string, opts: { query?: Query; body?: unknown } = {}): Promise<T> {
    const url = new URL(this.config.baseUrl + path);
    for (const [k, v] of Object.entries(opts.query ?? {})) {
      if (v !== undefined && v !== "") url.searchParams.set(k, String(v));
    }

    const res = await fetch(url, {
      method,
      headers: {
        Authorization: this.config.authHeader,
        Accept: "application/json",
        ...(opts.body !== undefined ? { "Content-Type": "application/json" } : {}),
      },
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
      signal: AbortSignal.timeout(30_000),
    });

    const text = await res.text();
    if (!res.ok) throw new Error(`Jira ${method} ${url.pathname} failed: ${res.status} ${res.statusText} - ${describeError(text)}`);
    return (text ? JSON.parse(text) : {}) as T;
  }

  issueUrl(key: string): string {
    return `${this.config.baseUrl}/browse/${key}`;
  }

  /** Cloud identifies users by accountId, Server/DC by username. */
  userRef(user: string | null): Record<string, string | null> {
    return this.config.isCloud ? { accountId: user } : { name: user };
  }
}

function describeError(text: string): string {
  try {
    const j = JSON.parse(text);
    const parts = [...(j.errorMessages ?? []), ...Object.entries(j.errors ?? {}).map(([k, v]) => `${k}: ${v}`)];
    if (parts.length) return parts.join("; ");
    if (j.message) return j.message;
  } catch {
    // not JSON
  }
  return text.slice(0, 500);
}
