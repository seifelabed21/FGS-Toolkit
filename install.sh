#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALL_DIR="${HOME}/.local/share/fgs-toolkit"
BIN_DIR="${HOME}/.local/bin"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required. Install Python 3, then run this installer again." >&2
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
    echo "Error: FGS Toolkit requires Python 3.9 or newer (found ${PYTHON_VERSION})." >&2
    exit 1
fi

mkdir -p "$INSTALL_DIR" "$BIN_DIR"
cp "$SCRIPT_DIR"/*.py "$INSTALL_DIR"/
cp "$SCRIPT_DIR"/README.md "$INSTALL_DIR"/

cat > "$BIN_DIR/fgs-toolkit" <<'EOF'
#!/bin/sh
exec python3 "$HOME/.local/share/fgs-toolkit/main.py" "$@"
EOF
chmod +x "$BIN_DIR/fgs-toolkit"

echo "FGS Toolkit installed. Run: fgs-toolkit"
case ":${PATH}:" in
    *":${BIN_DIR}:"*) ;;
    *) echo "If the command is not found, add this to your shell profile:"
       echo 'export PATH="$HOME/.local/bin:$PATH"' ;;
esac
