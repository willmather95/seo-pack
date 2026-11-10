#!/usr/bin/env bash
# Install or update the SEO pack skills as plain copies.
# Targets: ~/.claude/skills, ~/.codex/skills, ~/.agents/skills
# Safe to run again: it replaces only the pack's own skill folders. Anything else it would
# replace is copied to ~/skill-backups/<time>/ first. Nothing is deleted without a backup.
# Works on Linux and macOS (bash 3.2+). No network, no keys.
#
# Usage: ./install.sh            install or update
#        ./install.sh --check    show what is installed, change nothing
#        ./install.sh --uninstall remove the pack's skills from the targets
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
VERSION="$(cat "$HERE/VERSION" 2>/dev/null || echo dev)"
TARGETS="$HOME/.claude/skills $HOME/.codex/skills $HOME/.agents/skills"
# Grok Bot workflows folder (box only). Override with SEO_PACK_WORKFLOWS=/path, or set it empty to skip.
WORKFLOWS="${SEO_PACK_WORKFLOWS-/home/box/agent-data/workflows}"
# Pack skills that also get their own Grok Bot workflow folder (with scripts), not just a reference file.
STANDALONE="jev-seo-campaign seo-research-openseo"
# Optional shared skills, read from SEO_PACK_SHARED_SRC (default: ./shared). Skipped when missing.
# Set SEO_PACK_SHARED=1 or 0 to force.
SHARED="jev-decisions"
SHARED_SRC="${SEO_PACK_SHARED_SRC:-$HERE/shared}"
if [ -n "${SEO_PACK_SHARED:-}" ]; then DO_SHARED="$SEO_PACK_SHARED"
elif [ -d /home/box/agent-data ]; then DO_SHARED=0
else DO_SHARED=1; fi
BK="$HOME/skill-backups/$(date +%Y%m%d-%H%M%S)"
MODE="${1:-install}"

skills() { for d in "$HERE"/skills/*/; do [ -f "$d/SKILL.md" ] && basename "$d"; done; }

label() { echo "$1" | sed "s#^$HOME/##; s#/#_#g"; } # ~/.claude/skills -> .claude_skills

backup() { # path label: copy path (or the symlink itself) into the backup folder
  [ -e "$1" ] || [ -L "$1" ] || return 0
  mkdir -p "$BK/$2"
  cp -RP "$1" "$BK/$2/"
  echo "backed up $1 -> $BK/$2/$(basename "$1")"
}

copy_dir() { # src dest: replace dest with a fresh copy (a symlink at dest is replaced, not followed)
  if [ -L "$2" ] || { [ -e "$2" ] && [ ! -f "$2/.seo-pack-version" ]; }; then
    backup "$2" "$(label "$(dirname "$2")")"
  fi
  rm -rf "$2"
  mkdir -p "$(dirname "$2")"
  cp -R "$1" "$2"
}

case "$MODE" in
  --check)
    for t in $TARGETS; do
      for s in $(skills); do
        if [ -f "$t/$s/.seo-pack-version" ]; then v="$(cat "$t/$s/.seo-pack-version")"
        elif [ -e "$t/$s" ]; then v="present (not from install.sh)"
        else v="missing"; fi
        echo "$t/$s: $v"
      done
      for s in $SHARED; do
        if [ -L "$t/$s" ]; then v="symlink"
        elif [ ! -e "$t/$s" ]; then v="missing"
        elif [ -d "$SHARED_SRC/$s" ] && diff -rq "$SHARED_SRC/$s" "$t/$s" >/dev/null 2>&1; then v="matches repo"
        else v="differs from repo"; fi
        echo "$t/$s (shared): $v"
      done
    done
    if [ -n "$WORKFLOWS" ] && [ -d "$WORKFLOWS" ]; then
      for w in seo-pack $STANDALONE; do
        f="$WORKFLOWS/$w/.seo-pack-version"
        echo "$WORKFLOWS/$w: $( [ -f "$f" ] && cat "$f" || echo missing)"
      done
    fi
    echo "source version: $VERSION"
    exit 0 ;;
  --uninstall)
    for t in $TARGETS; do for s in $(skills); do
      [ -f "$t/$s/.seo-pack-version" ] && rm -rf "$t/$s" && echo "removed $t/$s"
    done; done
    exit 0 ;;
  install|--install) ;;
  *) echo "unknown option: $MODE"; exit 2 ;;
esac

for t in $TARGETS; do
  mkdir -p "$t"
  for s in $(skills); do
    copy_dir "$HERE/skills/$s" "$t/$s"
    echo "$VERSION" > "$t/$s/.seo-pack-version"
  done
  echo "installed $(skills | wc -l | tr -d ' ') skills into $t ($VERSION)"
  if [ "$DO_SHARED" = 1 ]; then
    for s in $SHARED; do
      src="$SHARED_SRC/$s"
      [ -f "$src/SKILL.md" ] || { echo "shared $s: not in $SHARED_SRC, skipped"; continue; }
      if [ -L "$t/$s" ]; then echo "shared $s: $t/$s is a symlink, left alone"; continue; fi
      if [ -e "$t/$s" ] && diff -rq "$src" "$t/$s" >/dev/null 2>&1; then echo "shared $s: $t/$s already matches"; continue; fi
      backup "$t/$s" "$(label "$t")"
      rm -rf "$t/$s"; cp -R "$src" "$t/$s"
      echo "shared $s: installed into $t"
    done
  fi
done

# Grok Bot: one workflow folder. SKILL.md is the loop; the other skills sit in references/.
if [ -n "$WORKFLOWS" ] && [ -d "$WORKFLOWS" ]; then
  W="$WORKFLOWS/seo-pack"
  rm -rf "$W"; mkdir -p "$W/references"
  { cat "$HERE/grok/HEADER.md"
    awk 'BEGIN{n=0} n>=2{print; next} /^---[[:space:]]*$/{n++; next} n<1{print}' "$HERE/skills/seo-loop/SKILL.md"
  } > "$W/SKILL.md"
  cp -R "$HERE/skills/seo-loop/sites" "$W/sites"
  # seo-loop's own reference files (for example seo-case-study.md) sit next to the other skills.
  if [ -d "$HERE/skills/seo-loop/references" ]; then cp "$HERE"/skills/seo-loop/references/*.md "$W/references/"; fi
  for s in $(skills); do
    [ "$s" = "seo-loop" ] || cp "$HERE/skills/$s/SKILL.md" "$W/references/$s.md"
  done
  echo "$VERSION" > "$W/.seo-pack-version"
  echo "installed Grok Bot workflow into $W ($VERSION)"
  for s in $STANDALONE; do
    [ -f "$HERE/skills/$s/SKILL.md" ] || continue
    copy_dir "$HERE/skills/$s" "$WORKFLOWS/$s"
    echo "$VERSION" > "$WORKFLOWS/$s/.seo-pack-version"
    echo "installed Grok Bot workflow into $WORKFLOWS/$s ($VERSION)"
  done
fi
echo "Done. Restart Claude Code and Codex to pick up changes."
