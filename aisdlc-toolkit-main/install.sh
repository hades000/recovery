#!/usr/bin/env bash
#
# install.sh - Install or update the SCBX AI-First SDLC toolkit in a product repository.
#
# Copies repo-template/ (agents, rules, prompts, templates, scripts, contexts folder,
# VS Code and Claude Code MCP configuration and the standard folder structure) into a
# product repository and points the Jira, Confluence and GitLab MCP servers at this toolkit.
#
# Usage:
#   ./install.sh <product-repo>            install; existing files are never overwritten
#   ./install.sh <product-repo> --update   also replace toolkit-owned files with this version
#   ./install.sh <product-repo> --dry-run  show what would be done
#
# Toolkit-owned files (replaced by --update): .github/agents, .github/rules,
# .github/prompts, .github/templates, .github/scripts, .github/instructions,
# .github/copilot-instructions.md, .claude/agents, .claude/commands, CLAUDE.md.
# Project-owned files (never overwritten): .github/contexts, .vscode/mcp.json,
# .mcp.json, docs, requirement, output, .gitignore.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly TEMPLATE_DIR="${SCRIPT_DIR}/repo-template"
readonly GITIGNORE_ENTRIES=(".env" ".claude/settings.local.json" "generated_tests/_mcp-artifacts/" "__pycache__/")

usage() {
  sed -n '9,18p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

log() {
  printf "%s\n" "$*"
}

err() {
  printf "ERROR: %s\n" "$1" >&2
  exit 1
}

is_toolkit_owned() {
  case "$1" in
    .github/agents/* | .github/rules/* | .github/prompts/* | .github/templates/* | \
      .github/scripts/* | .github/instructions/* | .github/copilot-instructions.md | \
      .claude/agents/* | .claude/commands/* | CLAUDE.md)
      return 0 ;;
    *)
      return 1 ;;
  esac
}

main() {
  local target="" update=false dry_run=false
  for arg in "$@"; do
    case "$arg" in
      --update) update=true ;;
      --dry-run) dry_run=true ;;
      -h | --help) usage; exit 0 ;;
      -*) err "Unknown option: $arg" ;;
      *) target="$arg" ;;
    esac
  done
  [[ -n "$target" ]] || { usage; err "Missing <product-repo>"; }
  [[ -d "$target" ]] || err "Target is not a directory: $target"
  [[ -d "$TEMPLATE_DIR" ]] || err "repo-template not found next to install.sh"

  target="$(cd "$target" && pwd)"
  local copied=0 replaced=0 skipped=0 rel src dst

  while IFS= read -r -d '' src; do
    rel="${src#"$TEMPLATE_DIR"/}"
    dst="${target}/${rel}"
    if [[ ! -e "$dst" ]]; then
      log "add      $rel"
      copied=$((copied + 1))
      $dry_run || { mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; }
    elif $update && is_toolkit_owned "$rel"; then
      if cmp -s "$src" "$dst"; then
        skipped=$((skipped + 1))
      else
        log "update   $rel"
        replaced=$((replaced + 1))
        $dry_run || cp "$src" "$dst"
      fi
    else
      skipped=$((skipped + 1))
    fi
  done < <(find "$TEMPLATE_DIR" -type f -print0)

  # Point the MCP servers at this toolkit (only when the file was just created).
  local mcp
  for mcp in "${target}/.vscode/mcp.json" "${target}/.mcp.json"; do
    if [[ -f "$mcp" ]] && grep -q "__TOOLKIT_DIR__" "$mcp"; then
      log "set      ${mcp#"$target"/} toolkit path -> ${SCRIPT_DIR}"
      $dry_run || {
        local tmp
        tmp="$(mktemp)"
        sed "s#__TOOLKIT_DIR__#${SCRIPT_DIR}#g" "$mcp" > "$tmp" && mv "$tmp" "$mcp"
      }
    fi
  done

  # Merge .gitignore entries without duplicating lines.
  local gitignore="${target}/.gitignore" entry
  for entry in "${GITIGNORE_ENTRIES[@]}"; do
    if [[ ! -f "$gitignore" ]] || ! grep -qxF "$entry" "$gitignore"; then
      log "ignore   $entry"
      $dry_run || printf "%s\n" "$entry" >> "$gitignore"
    fi
  done

  log ""
  log "Done: ${copied} added, ${replaced} updated, ${skipped} unchanged in ${target}"
  if [[ ! -f "${SCRIPT_DIR}/mcp/jira/dist/index.js" ]]; then
    log "Note: MCP servers are not built yet. Run: cd ${SCRIPT_DIR}/mcp && npm install && npm run build"
  fi
  log "Next: open the repository in VS Code, start the MCP servers (MCP: List Servers),"
  log "      create the increment card (docs/increments/) and run Context Builder."
}

main "$@"
