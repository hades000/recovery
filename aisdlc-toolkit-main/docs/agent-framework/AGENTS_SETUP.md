# Agents Setup

## Purpose
This folder defines GitHub Copilot agents for a generic spec-driven PDLC workflow, and the Claude
Code subagents generated from the same sources.

## Agent Files

```text
.github/agents/api-tester.agent.md
.github/agents/context-builder.agent.md
.github/agents/context-updater.agent.md
.github/agents/figma-extractor.agent.md
.github/agents/functional-automation-test.agent.md
.github/agents/implement.agent.md
.github/agents/planner.agent.md
.github/agents/qa-test-case-generator.agent.md
.github/agents/reviewer.agent.md
.github/agents/specify.agent.md
.github/agents/technical-documenter.agent.md
.github/agents/traceability-manager.agent.md
```

## How To Use
Open GitHub Copilot Chat and select the relevant agent from the agent picker.

In Claude Code, pick the kebab-case equivalent from the `@` typeahead, or name it in a prompt:
`@agent-technical-specifier`, `@agent-implementation-planner`, `@agent-compliance-reviewer`, and so
on. The Claude Code files under `.claude/agents/` are generated from the `.agent.md` sources with
`node .github/scripts/sync-claude-agents.mjs`; see [CLAUDE_CODE.md](CLAUDE_CODE.md).

For existing requirement documents, use the intake prompt:

```text
.github/prompts/intake-to-spec.prompt.md
```

For a new project or missing project context, start with:

```text
Context Builder
```

The intake workflow produces the BRD and detailed requirements artifacts.

## Reusable Prompt Workflows

Use these prompt files in Copilot Chat when supported:

```text
.github/prompts/intake-to-spec.prompt.md
.github/prompts/intake-to-implementation.prompt.md
```

The same runbooks are generated as Claude Code slash commands in `.claude/commands/`:
`/intake-to-spec` and `/intake-to-implementation`.
