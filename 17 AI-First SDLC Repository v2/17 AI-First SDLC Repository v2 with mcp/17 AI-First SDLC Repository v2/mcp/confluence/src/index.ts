#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { ConfluenceClient, loadConfig } from "./client.js";

const API = "/rest/api";
const STORAGE_HINT =
  "Body is Confluence storage format (XHTML), e.g. <h2>Title</h2><p>Text with <strong>bold</strong></p><ul><li>item</li></ul>, " +
  "tables with <table><tbody><tr><th>..</th></tr></tbody></table>, code with " +
  "<ac:structured-macro ac:name=\"code\"><ac:plain-text-body><![CDATA[...]]></ac:plain-text-body></ac:structured-macro>.";

let client: ConfluenceClient | undefined;
function confluence(): ConfluenceClient {
  return (client ??= new ConfluenceClient(loadConfig()));
}

async function run(fn: () => Promise<unknown>) {
  try {
    const data = await fn();
    return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
  } catch (e) {
    return { isError: true, content: [{ type: "text" as const, text: e instanceof Error ? e.message : String(e) }] };
  }
}

function storageToText(html: string): string {
  return html
    .replace(/<ac:plain-text-body><!\[CDATA\[([\s\S]*?)\]\]><\/ac:plain-text-body>/g, "\n```\n$1\n```\n")
    .replace(/<(br|\/p|\/h[1-6]|\/li|\/tr|\/div|\/blockquote)[^>]*>/gi, "\n")
    .replace(/<(td|th)[^>]*>/gi, " | ")
    .replace(/<li[^>]*>/gi, "- ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function summarize(c: any) {
  return {
    id: c.id,
    type: c.type,
    title: c.title,
    space: c.space?.key,
    version: c.version?.number,
    lastUpdated: c.version?.when,
    lastUpdatedBy: c.version?.by?.displayName,
    url: confluence().webUrl(c),
  };
}

function cursorFrom(next: string | undefined): string | null {
  if (!next) return null;
  return new URL(next, "http://x").searchParams.get("cursor");
}

const server = new McpServer({ name: "confluence", version: "1.0.0" });

server.registerTool(
  "confluence_search",
  {
    title: "Search Confluence",
    description:
      "Search Confluence content with CQL, e.g. 'type = page AND space = ENG AND title ~ \"onboarding\"', " +
      "'text ~ \"release notes\" ORDER BY lastmodified DESC', or 'ancestor = 12345'.",
    inputSchema: {
      cql: z.string().describe("CQL query"),
      limit: z.number().int().min(1).max(100).default(25),
      start: z.number().int().min(0).optional().describe("Offset (Server/DC)"),
      cursor: z.string().optional().describe("Pagination cursor from a previous result (Cloud)"),
    },
    annotations: { readOnlyHint: true },
  },
  ({ cql, limit, start, cursor }) =>
    run(async () => {
      const res = await confluence().request("GET", `${API}/content/search`, {
        query: { cql, limit, start, cursor, expand: "space,version" },
      });
      return {
        size: res.size,
        start: res.start,
        nextCursor: cursorFrom(res._links?.next),
        results: res.results.map(summarize),
      };
    }),
);

server.registerTool(
  "confluence_get_page",
  {
    title: "Get Confluence page",
    description:
      "Get a Confluence page by ID, or by space key + exact title. format='storage' returns raw XHTML (use before editing); " +
      "format='text' returns readable plain text.",
    inputSchema: {
      pageId: z.string().optional(),
      spaceKey: z.string().optional(),
      title: z.string().optional(),
      format: z.enum(["storage", "text"]).default("storage"),
      includeComments: z.boolean().default(false),
    },
    annotations: { readOnlyHint: true },
  },
  ({ pageId, spaceKey, title, format, includeComments }) =>
    run(async () => {
      const expand = "body.storage,version,space,ancestors";
      let page: any;
      if (pageId) {
        page = await confluence().request("GET", `${API}/content/${encodeURIComponent(pageId)}`, { query: { expand } });
      } else if (spaceKey && title) {
        const res = await confluence().request("GET", `${API}/content`, { query: { spaceKey, title, expand, type: "page" } });
        page = res.results?.[0];
        if (!page) throw new Error(`No page titled '${title}' in space ${spaceKey}`);
      } else {
        throw new Error("Provide pageId, or spaceKey + title");
      }

      const storage: string = page.body?.storage?.value ?? "";
      let comments;
      if (includeComments) {
        const res = await confluence().request("GET", `${API}/content/${page.id}/child/comment`, {
          query: { expand: "body.storage,version", depth: "all", limit: 100 },
        });
        comments = res.results.map((c: any) => ({
          id: c.id,
          author: c.version?.by?.displayName,
          created: c.version?.when,
          body: storageToText(c.body?.storage?.value ?? ""),
        }));
      }

      return {
        ...summarize(page),
        ancestors: page.ancestors?.map((a: any) => ({ id: a.id, title: a.title })),
        body: format === "text" ? storageToText(storage) : storage,
        comments,
      };
    }),
);

server.registerTool(
  "confluence_get_page_children",
  {
    title: "List child pages",
    description: "List direct child pages of a Confluence page.",
    inputSchema: {
      pageId: z.string(),
      limit: z.number().int().min(1).max(200).default(50),
      start: z.number().int().min(0).optional(),
    },
    annotations: { readOnlyHint: true },
  },
  ({ pageId, limit, start }) =>
    run(async () => {
      const res = await confluence().request("GET", `${API}/content/${encodeURIComponent(pageId)}/child/page`, {
        query: { limit, start, expand: "version,space" },
      });
      return res.results.map(summarize);
    }),
);

server.registerTool(
  "confluence_list_spaces",
  {
    title: "List Confluence spaces",
    description: "List Confluence spaces visible to the user.",
    inputSchema: {
      type: z.enum(["global", "personal"]).optional(),
      limit: z.number().int().min(1).max(200).default(50),
      start: z.number().int().min(0).optional(),
    },
    annotations: { readOnlyHint: true },
  },
  ({ type, limit, start }) =>
    run(async () => {
      const res = await confluence().request("GET", `${API}/space`, { query: { type, limit, start } });
      return res.results.map((s: any) => ({ key: s.key, name: s.name, type: s.type, url: confluence().webUrl(s) }));
    }),
);

server.registerTool(
  "confluence_create_page",
  {
    title: "Create Confluence page",
    description: `Create a new Confluence page in a space, optionally under a parent page. ${STORAGE_HINT}`,
    inputSchema: {
      spaceKey: z.string(),
      title: z.string(),
      body: z.string().describe("Page content in storage format (XHTML)"),
      parentId: z.string().optional().describe("Parent page ID"),
    },
  },
  ({ spaceKey, title, body, parentId }) =>
    run(async () => {
      const page = await confluence().request("POST", `${API}/content`, {
        body: {
          type: "page",
          title,
          space: { key: spaceKey },
          ...(parentId && { ancestors: [{ id: parentId }] }),
          body: { storage: { value: body, representation: "storage" } },
        },
      });
      return summarize(page);
    }),
);

server.registerTool(
  "confluence_update_page",
  {
    title: "Update Confluence page",
    description:
      `Update a Confluence page's title and/or content. mode='replace' overwrites the body; 'append'/'prepend' add to existing content ` +
      `(safer for large pages). ${STORAGE_HINT}`,
    inputSchema: {
      pageId: z.string(),
      title: z.string().optional(),
      body: z.string().optional().describe("Content in storage format (XHTML)"),
      mode: z.enum(["replace", "append", "prepend"]).default("replace"),
      versionComment: z.string().optional(),
      minorEdit: z.boolean().default(false).describe("Minor edits don't notify watchers"),
    },
  },
  ({ pageId, title, body, mode, versionComment, minorEdit }) =>
    run(async () => {
      if (title === undefined && body === undefined) throw new Error("Provide title and/or body");
      const path = `${API}/content/${encodeURIComponent(pageId)}`;
      const current = await confluence().request("GET", path, { query: { expand: "body.storage,version,space" } });
      const existing: string = current.body?.storage?.value ?? "";
      const newBody =
        body === undefined ? existing : mode === "append" ? existing + body : mode === "prepend" ? body + existing : body;

      const page = await confluence().request("PUT", path, {
        body: {
          id: current.id,
          type: current.type,
          title: title ?? current.title,
          space: { key: current.space?.key },
          version: { number: current.version.number + 1, minorEdit, ...(versionComment && { message: versionComment }) },
          body: { storage: { value: newBody, representation: "storage" } },
        },
      });
      return summarize(page);
    }),
);

server.registerTool(
  "confluence_add_comment",
  {
    title: "Add Confluence comment",
    description: "Add a footer comment to a Confluence page. Body in storage format, e.g. <p>Looks good</p>.",
    inputSchema: { pageId: z.string(), body: z.string() },
  },
  ({ pageId, body }) =>
    run(async () => {
      const comment = await confluence().request("POST", `${API}/content`, {
        body: {
          type: "comment",
          container: { id: pageId, type: "page" },
          body: { storage: { value: body, representation: "storage" } },
        },
      });
      return { id: comment.id, pageId, url: confluence().webUrl(comment) };
    }),
);

await server.connect(new StdioServerTransport());
console.error("Confluence MCP server running on stdio");
