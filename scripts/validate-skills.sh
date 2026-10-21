#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# This repo is a Claude Code plugin marketplace: a root marketplace.json
# points at the bundled plugin under plugins/, whose skills live in
# plugins/<plugin>/skills/<name>/SKILL.md. Validate them all.

marketplace="$repo_root/.claude-plugin/marketplace.json"
if [[ ! -f "$marketplace" ]]; then
  echo "Missing marketplace manifest: $marketplace" >&2
  exit 1
fi

# Validate JSON manifests if a JSON parser is available.
json_check() {
  local f="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" \
      || { echo "Invalid JSON: $f" >&2; exit 1; }
  fi
}
json_check "$marketplace"
while IFS= read -r manifest; do
  json_check "$manifest"
done < <(find "$repo_root/plugins" -name plugin.json -type f 2>/dev/null | sort)

# The root .claude-plugin/plugin.json mirrors the plugin's manifest so the
# plugin directory submission (plugin path = repository root) finds a plugin;
# only its paths differ. Fail if the two drift apart.
root_manifest="$repo_root/.claude-plugin/plugin.json"
plugin_manifest="$repo_root/plugins/letradalei/.claude-plugin/plugin.json"
if [[ -f "$root_manifest" ]] && command -v python3 >/dev/null 2>&1; then
  json_check "$root_manifest"
  python3 - "$root_manifest" "$plugin_manifest" <<'PY' || exit 1
import json, sys
root, plugin = (json.load(open(p)) for p in sys.argv[1:])
paths = {"icon", "skills", "mcpServers"}
drift = sorted(k for k in (root.keys() | plugin.keys()) - paths if root.get(k) != plugin.get(k))
if drift:
    sys.exit("Root plugin.json drifted from plugins/letradalei: " + ", ".join(drift))
PY
fi

skill_files=()
while IFS= read -r skill_file; do
  skill_files+=("$skill_file")
done < <(find "$repo_root" -name SKILL.md -type f -not -path '*/.git/*' | sort)

if [[ "${#skill_files[@]}" -eq 0 ]]; then
  echo "No SKILL.md files found under $repo_root" >&2
  exit 1
fi

for skill_file in "${skill_files[@]}"; do
  if ! grep -q '^name:' "$skill_file"; then
    echo "Missing name frontmatter in $skill_file" >&2
    exit 1
  fi

  if ! grep -q '^description:' "$skill_file"; then
    echo "Missing description frontmatter in $skill_file" >&2
    exit 1
  fi

  # Skill name must be bare kebab-case, the plugin namespace is applied
  # automatically at invocation, so a colon in the name field is invalid.
  if grep -qE '^name:.*:' "$skill_file"; then
    echo "Skill name must not contain a colon (use bare kebab-case): $skill_file" >&2
    exit 1
  fi
done

echo "Validated ${#skill_files[@]} skill(s) and the marketplace manifest."
