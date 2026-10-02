
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-8000}"
URL="http://127.0.0.1:${PORT}"


pause_on_error() {
  echo ""
  read -r -p "Press Return to close this window..."
}
is_our_dashboard() {
  curl -s --max-time 2 "${URL}/api/data" 2>/dev/null | grep -q '"problems"'
}

PYTHON=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
else
  for c in /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
    if [ -x "$c" ]; then PYTHON="$c"; break; fi
  done
fi
if [ -z "$PYTHON" ]; then
  echo "ERROR: Couldn't find python3."
  echo "Install it (python.org, or 'brew install python') and try again."
  pause_on_error
  exit 1
fi

if is_our_dashboard; then
  echo "Dashboard already running at ${URL} — opening your browser."
  open "$URL"
  exit 0
fi

# --- start the server 
SERVER_PID=""
cleanup() {
  if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null
    echo "Dashboard stopped (port ${PORT} freed)."
  fi
}
trap cleanup INT TERM EXIT

echo "Starting Qusay Coding Problems Dashboard on ${URL}"
echo "Press Ctrl+C to stop (or just close this window)."
"$PYTHON" "$DIR/server.py" "$PORT" &
SERVER_PID=$!

up=""
for _ in 1 2 3 4 5 6 7 8 9 10; do
  if is_our_dashboard; then up="yes"; break; fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then break; fi   # server exited early
  sleep 0.5
done

if [ -z "$up" ]; then
  echo ""
  echo "ERROR: the server didn't come up on port ${PORT}."
  echo "The port may already be in use by another program, or server.py failed to start."
  echo "Try a different port by running this in Terminal:"
  echo "  \"$DIR/start-dashboard.command\" 8001"
  pause_on_error
  exit 1
fi

open "$URL"
wait "$SERVER_PID"
