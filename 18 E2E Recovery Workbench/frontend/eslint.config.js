import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

// D-RCV-39 import allow-list for frontend/src/modules/recovery/**. Outside the folder only the
// shared ACE entry points are allowed; inside it, @/modules/recovery/** and ./ paths. ../ and the
// rest of @/ are forbidden. The same rule runs in the ACE front end.
const recoveryImportRule = {
  "no-restricted-imports": [
    "error",
    {
      patterns: [
        {
          group: ["../*", "../**"],
          message: "D-RCV-39: no ../ imports in the recovery module. Use @/modules/recovery/** or ./",
        },
        {
          // SEC-TE001-01: a `..` segment must not hide behind an allowed prefix
          // (e.g. @/components/ui/../../modules/collection). The leading-`../` group above
          // already reports that form, so exclude it here to keep one message per import.
          regex: "^(?!\\.\\./).*\\.\\.",
          message: "D-RCV-39: no '..' path segments in the recovery module.",
        },
        {
          regex: "^@/(?!components/ui/|lib/utils$|utils/(?!cfsc)[^/]+$|contexts/ApiClientContext$|api/schema$|modules/recovery/)",
          message:
            "D-RCV-39: outside the recovery folder only @/components/ui/**, @/lib/utils, @/utils/* (not cfsc*), @/contexts/ApiClientContext and @/api/schema are allowed.",
        },
      ],
    },
  ],
};

export default tseslint.config(
  { ignores: ["dist", "coverage", "playwright-report", "test-results", "src/api/schema.d.ts"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: { ecmaVersion: 2022, globals: globals.browser },
    plugins: { "react-hooks": reactHooks },
    rules: {
      ...reactHooks.configs.recommended.rules,
    },
  },
  {
    files: ["src/modules/recovery/**/*.{ts,tsx}"],
    rules: recoveryImportRule,
  },
);
