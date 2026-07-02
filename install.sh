#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/colchuck-ai/agent-skill-review.git"
BRANCH="main"
AGENT="cursor"
DEST=""

usage() {
  cat <<'EOF'
Install the agent-skill-review Agent Skill.

Usage: install.sh [--agent <name>] [DIR]

Options:
  --agent <name>   Install into a known agent's skills directory:
                     cursor   ~/.cursor/skills/agent-skill-review   (default)
                     claude   ~/.claude/skills/agent-skill-review
                     agents   ~/.agents/skills/agent-skill-review
  -h, --help       Show this help.

Arguments:
  DIR              Install directly into DIR, overriding --agent.

Examples:
  install.sh                                              # ~/.cursor/skills/agent-skill-review
  install.sh --agent claude                               # ~/.claude/skills/agent-skill-review
  install.sh ~/.config/my-agent/skills/agent-skill-review # custom directory

When piping from curl, pass options after `-s --`:
  curl -fsSL <url>/install.sh | bash -s -- --agent claude
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --agent) AGENT="${2:-}"; shift 2 ;;
    --agent=*) AGENT="${1#*=}"; shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *) DEST="$1"; shift ;;
  esac
done

# A directory may also follow `--`.
if [ -z "$DEST" ] && [ $# -gt 0 ]; then
  DEST="$1"
fi

# Resolve the destination from the agent when no explicit directory is given.
if [ -z "$DEST" ]; then
  case "$AGENT" in
    cursor) DEST="$HOME/.cursor/skills/agent-skill-review" ;;
    claude) DEST="$HOME/.claude/skills/agent-skill-review" ;;
    agents) DEST="$HOME/.agents/skills/agent-skill-review" ;;
    *) echo "Unknown agent: $AGENT" >&2; usage >&2; exit 1 ;;
  esac
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMP/agent-skill-review"

rm -rf "$DEST"
mkdir -p "$DEST"
cp -R "$TMP/agent-skill-review/agent-skill-review/" "$DEST/"
cp -R "$TMP/agent-skill-review/LICENSE" "$DEST/"

echo "Installed agent-skill-review skill to $DEST"
