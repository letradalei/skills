#!/usr/bin/env bash
# Builds conformidade-local from the platform worktree's internal/conformidade without writing to it
# (go build -overlay maps main.go into services/gateway/cmd/backtestconformidade virtually).
# Usage: build.sh <platform-worktree> <out-binary>
set -euo pipefail
PLATFORM=${1:?platform worktree}
OUT=${2:?output binary}
HERE=$(cd "$(dirname "$0")" && pwd)
GW="$PLATFORM/services/gateway"
OV=$(mktemp)
trap 'rm -f "$OV"' EXIT
printf '{"Replace":{"%s/cmd/backtestconformidade/main.go":"%s/main.go"}}' "$GW" "$HERE" > "$OV"
(cd "$GW" && go build -overlay "$OV" -o "$OUT" ./cmd/backtestconformidade)
# wrapper: read-only session on the direct (non-pooler) endpoint; refuses fixed branches by name check
cat > "$OUT.sh" <<'WRAP'
#!/usr/bin/env bash
set -euo pipefail
URL=${PRODCOPY_DATABASE_URL:?PRODCOPY_DATABASE_URL (Neon TEST branch) not set}
case "$URL" in *production*|*prod-*|*beta*) echo "refusing a non-test database URL" >&2; exit 2;; esac
URL=${URL/-pooler./.}
# no AWS credentials locally: fail the Bedrock query embedding fast so conceito(query) uses its lexical fallback
export AWS_EC2_METADATA_DISABLED=true
SEP='&'; [[ "$URL" == *\?* ]] || SEP='?'
export PRODCOPY_DATABASE_URL="${URL}${SEP}options=-c%20default_transaction_read_only%3Don"
"$(dirname "$0")/conformidade-local" "$@" | grep -v '^{"_aws"'
exit "${PIPESTATUS[0]}"
WRAP
chmod +x "$OUT.sh"
echo "built $OUT and $OUT.sh"
