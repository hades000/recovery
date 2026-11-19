// @vitest-environment node
import { fileURLToPath } from "node:url";
import path from "node:path";
import { describe, it, expect, beforeAll } from "vitest";
import { ESLint } from "eslint";

// RWB-TE-001 SPEC-015, AC6 (T-TE001-07): the D-RCV-39 import allow-list lives in the real
// eslint.config.js. Each fixture is an in-memory source file under src/modules/recovery/, so the
// recovery block applies; no fixture file is written to disk.
const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");
const fixturePath = "src/modules/recovery/caselist/BoundaryFixture.tsx";

const rejected = [
  "@/modules/collection/worklist/WorkList",
  "../../collection/worklist/WorkList",
  "@/hooks/cfsc/x",
  "@/api/tdr/config",
  "@/pages/x",
  "@/utils/cfscCaseList",
  "@/modules/other/x",
  "../x",
  "@/components/ui/../../modules/collection/worklist/WorkList",
  "@/modules/recovery/../../collection/worklist/WorkList",
  "./../collection/worklist/WorkList",
];

const allowed = [
  "@/components/ui/button",
  "@/lib/utils",
  "@/utils/date",
  "@/contexts/ApiClientContext",
  "@/api/schema",
  "@/modules/recovery/casewf/x",
  "./sibling",
];

let eslint: ESLint;

async function restrictedMessages(specifier: string): Promise<number> {
  const source = `import value from "${specifier}";\nexport const used = value;\n`;
  const results = await eslint.lintText(source, { filePath: fixturePath });
  const result = results[0];
  if (!result) {
    throw new Error(`ESLint returned no result for ${specifier}`);
  }
  return result.messages.filter((message) => message.ruleId === "no-restricted-imports").length;
}

describe("D-RCV-39 import boundary", () => {
  beforeAll(() => {
    eslint = new ESLint({ cwd: frontendRoot });
  }, 30_000);

  it.each(rejected)("rejects %s", async (specifier) => {
    expect(await restrictedMessages(specifier)).toBe(1);
  });

  it.each(allowed)("allows %s", async (specifier) => {
    expect(await restrictedMessages(specifier)).toBe(0);
  });
}, 30_000);
