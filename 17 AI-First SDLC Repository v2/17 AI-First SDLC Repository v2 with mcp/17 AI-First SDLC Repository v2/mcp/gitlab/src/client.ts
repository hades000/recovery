import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Optional per-server .env (mcp/gitlab/.env); variables already set by the MCP client take precedence.
const envFile = resolve(dirname(fileURLToPath(import.meta.url)), "..", ".env");
if (existsSync(envFile)) process.loadEnvFile(envFile);

export interface GitLabConfig {
  baseUrl: string;
  token: string;
}

export function loadConfig(): GitLabConfig {
  const url = process.env.GITLAB_URL?.trim();
  if (!url) throw new Error("GITLAB_URL is not set (e.g. https://gitlab.your-company.com)");
  const token = process.env.GITLAB_TOKEN?.trim();
  if (!token) throw new Error("GITLAB_TOKEN is not set (Personal Access Token with 'api' or 'read_api' scope)");
  return { baseUrl: url.replace(/\/+$/, ""), token };
}

type Query = Record<string, string | number | boolean | undefined>;
interface RequestOptions {
  query?: Query;
  body?: unknown;
}

export class GitLabClient {
  constructor(readonly config: GitLabConfig) {}

  private async send(method: string, path: string, opts: RequestOptions = {}) {
    const url = new URL(`${this.config.baseUrl}/api/v4${path}`);
    for (const [k, v] of Object.entries(opts.query ?? {})) {
      if (v !== undefined && v !== "") url.searchParams.set(k, String(v));
    }

    const res = await fetch(url, {
      method,
      headers: {
        "PRIVATE-TOKEN": this.config.token,
        Accept: "application/json",
        ...(opts.body !== undefined ? { "Content-Type": "application/json" } : {}),
      },
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
      signal: AbortSignal.timeout(60_000),
    });

    const text = await res.text();
    if (!res.ok) {
      const err = new Error(`GitLab ${method} ${url.pathname} failed: ${res.status} ${res.statusText} - ${describeError(text)}`);
      (err as Error & { status?: number }).status = res.status;
      throw err;
    }
    return { res, text };
  }

  async request<T = any>(method: string, path: string, opts: RequestOptions = {}): Promise<T> {
    const { text } = await this.send(method, path, opts);
    return (text ? JSON.parse(text) : {}) as T;
  }

  /** GET a paginated list; nextPage is null on the last page. */
  async list<T = any>(path: string, query: Query = {}): Promise<{ items: T[]; nextPage: number | null }> {
    const { res, text } = await this.send("GET", path, { query });
    const next = res.headers.get("x-next-page");
    return { items: JSON.parse(text) as T[], nextPage: next ? Number(next) : null };
  }

  async raw(path: string, query: Query = {}): Promise<string> {
    return (await this.send("GET", path, { query })).text;
  }
}

/** Accepts a numeric project ID or a full path like "group/subgroup/project". */
export function projectPath(project: string): string {
  return `/projects/${encodeURIComponent(project)}`;
}

function describeError(text: string): string {
  try {
    const j = JSON.parse(text);
    const msg = j.message ?? j.error;
    if (msg) return typeof msg === "string" ? msg : JSON.stringify(msg);
  } catch {
    // not JSON
  }
  return text.slice(0, 500);
}
