#!/usr/bin/env bash
# Render helper for Longxia Vlog HyperFrames projects.

set -euo pipefail

PROJECT_DIR="."
FPS="24"
SKIP_VALIDATE="0"
SKIP_INSPECT="0"
HYPERFRAMES_PACKAGE="${HYPERFRAMES_PACKAGE:-hyperframes@0.6.46}"

usage() {
  cat <<'USAGE'
Usage:
  render-vlog.sh <project-dir> [--preview|--final] [--fps N] [--skip-validate] [--skip-inspect]

Defaults:
  --final   24fps
  --preview 10fps

Expected project files:
  index.html
  assets/bgm.mp3 or assets/bgm.wav
  assets/voice-*.mp3 or assets/voice-*.wav
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --preview)
      FPS="10"
      shift
      ;;
    --final)
      FPS="24"
      shift
      ;;
    --fps)
      FPS="${2:-}"
      if ! [[ "$FPS" =~ ^[0-9]+$ ]]; then
        echo "Invalid --fps value: $FPS" >&2
        exit 2
      fi
      shift 2
      ;;
    --skip-validate)
      SKIP_VALIDATE="1"
      shift
      ;;
    --skip-inspect)
      SKIP_INSPECT="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      PROJECT_DIR="$1"
      shift
      ;;
  esac
done

cd "$PROJECT_DIR"

echo "Longxia Vlog render"
echo "Project: $(pwd)"
echo "FPS: $FPS"

if [ ! -f "index.html" ]; then
  echo "Missing index.html" >&2
  exit 1
fi

if [ ! -f "assets/bgm.mp3" ] && [ ! -f "assets/bgm.wav" ]; then
  echo "Missing BGM: assets/bgm.mp3 or assets/bgm.wav" >&2
  exit 1
fi

VOICE_COUNT=$(find assets -maxdepth 1 \( -name 'voice-*.mp3' -o -name 'voice-*.wav' \) | wc -l | tr -d ' ')
if [ "$VOICE_COUNT" = "0" ]; then
  echo "Missing voice files: assets/voice-*.mp3 or assets/voice-*.wav" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "Missing npx; install Node.js before rendering." >&2
  exit 1
fi

run_hyperframes() {
  npx --yes --package "$HYPERFRAMES_PACKAGE" hyperframes "$@"
}

echo "Voice files: $VOICE_COUNT"
echo "HyperFrames package: $HYPERFRAMES_PACKAGE"

if command -v ffprobe >/dev/null 2>&1; then
  echo "Voice durations:"
  find assets -maxdepth 1 \( -name 'voice-*.mp3' -o -name 'voice-*.wav' \) -print | sort | while read -r file; do
    duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file" || true)
    printf "  %s %.2fs\n" "$file" "${duration:-0}"
  done
else
  echo "ffprobe not found; skipping duration report."
fi

if [ "$SKIP_VALIDATE" = "0" ]; then
  echo "Running HyperFrames lint..."
  run_hyperframes lint

  if [ "$SKIP_INSPECT" = "0" ]; then
    echo "Running HyperFrames visual inspect..."
    run_hyperframes inspect --samples 12 --json
  fi

  echo "Running HyperFrames validation..."
  run_hyperframes validate
fi

echo "Rendering..."
run_hyperframes render --fps "$FPS"

LATEST=""
if [ -d "renders" ]; then
  LATEST=$(find renders -maxdepth 1 -type f -name '*.mp4' -exec ls -t {} + 2>/dev/null | head -1 || true)
fi

if [ -n "$LATEST" ]; then
  echo "Latest render: $LATEST"
  ls -lh "$LATEST"
else
  echo "Render command finished, but no mp4 was found under renders/." >&2
  exit 1
fi
