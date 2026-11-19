import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Optional per-server .env (mcp/confluence/.env); variables already set by the MCP client take precedence.
const envFile = resolve(dirname(fileURLToPath(import.meta.url)), "..", ".env");
if (existsSync(envFile)) process.loadEnvFile(envFile);

export interface ConfluenceConfig {
  baseUrl: string;
  authHeader: string;
}

export function loadConfig(): ConfluenceConfig {
  const url = process.env.CONFLUENCE_URL?.trim();
  if (!url) {
    throw new Error("CONFLUENCE_URL is not set (Cloud: https://your-company.atlassian.net/wiki, Server/DC: https://confluence.your-company.com)");
  }
  const baseUrl = url.replace(/\/+$/, "");

  const email = process.env.CONFLUENCE_EMAIL?.trim();
  const apiToken = process.env.CONFLUENCE_API_TOKEN?.trim();
  const pat = process.env.CONFLUENCE_PAT?.trim();

  let authHeader: string;
  if (email && apiToken) {
    authHeader = "Basic " + Buffer.from(`${email}:${apiToken}`).toString("base64");
  } else if (pat) {
    authHeader = `Bearer ${pat}`;
  } else {
    throw new Error("Set CONFLUENCE_EMAIL + CONFLUENCE_API_TOKEN (Confluence Cloud) or CONFLUENCE_PAT (Confluence Server/Data Center)");
  }

  return { baseUrl, authHeader };
}

type Query = Record<string, string | number | boolean | undefined>;

export class ConfluenceClient {
  constructor(readonly config: ConfluenceConfig) {}

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
    if (!res.ok) throw new Error(`Confluence ${method} ${url.pathname} failed: ${res.status} ${res.statusText} - ${describeError(text)}`);
    return (text ? JSON.parse(text) : {}) as T;
  }

  webUrl(content: any): string | undefined {
    const webui = content?._links?.webui;
    return webui ? (content._links.base ?? this.config.baseUrl) + webui : undefined;
  }
}

function describeError(text: string): string {
  try {
    const j = JSON.parse(text);
    if (j.message) return j.message;
  } catch {
    // not JSON
  }
  return text.slice(0, 500);
}
