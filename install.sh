#!/usr/bin/env bash
set -euo pipefail

OWNER="Jonnys-Li"
REPO="software-thesis-docx-skill"
REF="main"
DEST=""
NAME="software-thesis-docx"
FORCE=0

usage() {
  cat <<'EOF'
Usage: install.sh [--ref <ref>] [--dest <skills-dir>] [--name <skill-name>] [--force]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref)
      REF="${2:?missing value for --ref}"
      shift 2
      ;;
    --dest)
      DEST="${2:?missing value for --dest}"
      shift 2
      ;;
    --name)
      NAME="${2:?missing value for --name}"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3 is required to install this skill." >&2
  exit 1
fi

LOCAL_INSTALL_PY=""
TEMP_FILE=""

cleanup() {
  if [[ -n "${TEMP_FILE}" && -f "${TEMP_FILE}" ]]; then
    rm -f "${TEMP_FILE}"
  fi
}
trap cleanup EXIT

if [[ -n "${BASH_SOURCE:-}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" 2>/dev/null && pwd || true)"
  if [[ -n "${SCRIPT_DIR}" && -f "${SCRIPT_DIR}/install.py" ]]; then
    LOCAL_INSTALL_PY="${SCRIPT_DIR}/install.py"
  fi
fi

if [[ -n "${LOCAL_INSTALL_PY}" ]]; then
  INSTALL_PY="${LOCAL_INSTALL_PY}"
else
  RAW_URL="https://raw.githubusercontent.com/${OWNER}/${REPO}/${REF}/install.py"
  TEMP_FILE="$(mktemp)"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${RAW_URL}" -o "${TEMP_FILE}"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "${TEMP_FILE}" "${RAW_URL}"
  else
    echo "curl or wget is required to download the installer." >&2
    exit 1
  fi
  INSTALL_PY="${TEMP_FILE}"
fi

ARGS=(--ref "${REF}" --name "${NAME}")
if [[ -n "${DEST}" ]]; then
  ARGS+=(--dest "${DEST}")
fi
if [[ "${FORCE}" -eq 1 ]]; then
  ARGS+=(--force)
fi

"${PYTHON_BIN}" "${INSTALL_PY}" "${ARGS[@]}"
