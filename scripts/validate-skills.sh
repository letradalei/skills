#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/skills"

if [[ ! -d "$skills_dir" ]]; then
  echo "Missing skills directory: $skills_dir" >&2
  exit 1
fi

skill_files=()
while IFS= read -r skill_file; do
  skill_files+=("$skill_file")
done < <(find "$skills_dir" -name SKILL.md -type f | sort)

if [[ "${#skill_files[@]}" -eq 0 ]]; then
  echo "No SKILL.md files found under $skills_dir" >&2
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
done

echo "Validated ${#skill_files[@]} skill(s)."
