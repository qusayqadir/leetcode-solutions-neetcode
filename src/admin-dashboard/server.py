#!/usr/bin/env python3
"""
Local admin dashboard for LeetCode / NeetCode solutions.

- Serves the static UI from ./static
- Scans the repo's DSA/ and SQL/ folders (folders are the source of truth)
- Stores extra metadata (tags, notes, links, dates) in ./data.json
- Adding a problem with code writes a real .py/.sql file into the repo

Run:  python3 src/admin-dashboard/server.py  [port]
No dependencies beyond the Python 3 standard library.
"""

import json
import os
import re
import sys
import threading
import uuid
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))          # .../src/admin-dashboard
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))          # repo root
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")

# Folders scanned as problem collections. ext = file extension for new files.
COLLECTIONS = {
    "DSA": ".py",
    "SQL": ".sql",
}

# Difficulty: on-disk folder name  ->  display label
FOLDER_TO_DIFF = {"easy": "easy", "med": "medium", "medium": "medium", "hard": "hard"}
# Display label -> on-disk folder name (keeps new mediums in the existing "med/" folders)
DIFF_TO_FOLDER = {"easy": "easy", "medium": "med", "hard": "hard"}

_lock = threading.Lock()
_NUM_RE = re.compile(r"^\s*(\d+)\s*\.\s*(.*)$")


# ---------------------------------------------------------------------------
# data.json helpers
# ---------------------------------------------------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tags": [], "problems": {}, "topics": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("tags", [])
    data.setdefault("problems", {})
    data.setdefault("topics", [])
    return data


def save_data(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)


# ---------------------------------------------------------------------------
# Scanning the repo
# ---------------------------------------------------------------------------
def parse_name(stem):
    """'110. Balanced Binary Tree' -> (110, 'Balanced Binary Tree')."""
    m = _NUM_RE.match(stem)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return None, stem.strip()


def scan_files():
    """Walk DSA/ and SQL/ and return {relpath: problem_dict}."""
    found = {}
    for collection, ext in COLLECTIONS.items():
        root = os.path.join(REPO_ROOT, collection)
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if not fn.endswith(ext) or fn.startswith("."):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, REPO_ROOT).replace(os.sep, "/")
                parts = rel.split("/")
                # parts[0] = collection, parts[1] = topic (if any), last = filename
                topic = parts[1] if len(parts) >= 3 else "Misc"
                difficulty = "unknown"
                for p in parts[2:-1]:
                    if p.lower() in FOLDER_TO_DIFF:
                        difficulty = FOLDER_TO_DIFF[p.lower()]
                        break
                number, title = parse_name(os.path.splitext(fn)[0])
                try:
                    with open(full, "r", encoding="utf-8", errors="replace") as f:
                        code = f.read()
                except OSError:
                    code = ""
                found[rel] = {
                    "id": rel,
                    "collection": collection,
                    "topic": topic,
                    "difficulty": difficulty,
                    "number": number,
                    "title": title,
                    "code": code,
                    "hasFile": True,
                    "path": rel,
                }
    return found


def build_model():
    """Merge scanned files with sidecar metadata into the full client model."""
    data = load_data()
    scanned = scan_files()
    problems = []

    meta = data["problems"]
    for rel, prob in scanned.items():
        m = meta.get(rel, {})
        prob = dict(prob)
        prob["tags"] = m.get("tags", [])
        prob["notes"] = m.get("notes", "")
        prob["link"] = m.get("link", "")
        prob["date"] = m.get("date")  # None = imported / no date
        problems.append(prob)

    # Metadata-only problems (link-only entries with no file on disk)
    for pid, m in meta.items():
        if m.get("fileLess"):
            problems.append({
                "id": pid,
                "collection": m.get("collection", "DSA"),
                "topic": m.get("topic", "Misc"),
                "difficulty": m.get("difficulty", "unknown"),
                "number": m.get("number"),
                "title": m.get("title", pid),
                "code": m.get("code", ""),
                "hasFile": False,
                "path": None,
                "tags": m.get("tags", []),
                "notes": m.get("notes", ""),
                "link": m.get("link", ""),
                "date": m.get("date"),
            })

    # Topics per collection = scanned topics + user-created topics
    topics = {c: set() for c in COLLECTIONS}
    for p in problems:
        topics.setdefault(p["collection"], set()).add(p["topic"])
    for t in data["topics"]:
        topics.setdefault(t.get("collection", "DSA"), set()).add(t.get("name", ""))
    topics_out = {c: sorted(x for x in s if x) for c, s in topics.items()}

    return {
        "problems": problems,
        "tags": data["tags"],
        "topics": topics_out,
        "collections": list(COLLECTIONS.keys()),
    }


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------
def _sanitize_filename(s):
    return re.sub(r'[\\/:*?"<>|]', "-", s).strip()


def add_problem(body):
    collection = body.get("collection", "DSA")
    if collection not in COLLECTIONS:
        return 400, {"error": "unknown collection"}
    topic = (body.get("topic") or "").strip()
    if not topic:
        return 400, {"error": "topic is required"}
    title = (body.get("title") or "").strip()
    if not title:
        return 400, {"error": "title is required"}
    difficulty = body.get("difficulty", "unknown")
    code = body.get("code") or ""
    link = (body.get("link") or "").strip()
    notes = body.get("notes") or ""
    tags = body.get("tags") or []
    pdate = body.get("date") or date.today().isoformat()

    with _lock:
        data = load_data()

        if code.strip():
            # Write a real file into the repo.
            ext = COLLECTIONS[collection]
            diff_folder = DIFF_TO_FOLDER.get(difficulty)
            parts = [REPO_ROOT, collection, _sanitize_filename(topic)]
            if diff_folder:
                parts.append(diff_folder)
            folder = os.path.join(*parts)
            # The name field already contains the number (e.g. "1. Two Sum").
            fname = _sanitize_filename(title) + ext
            full = os.path.join(folder, fname)
            rel = os.path.relpath(full, REPO_ROOT).replace(os.sep, "/")
            if os.path.exists(full):
                return 409, {"error": f"file already exists: {rel}"}
            os.makedirs(folder, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(code if code.endswith("\n") else code + "\n")
            data["problems"][rel] = {
                "tags": tags, "notes": notes, "link": link, "date": pdate,
            }
            save_data(data)
            return 200, {"ok": True, "id": rel}
        else:
            # No code -> metadata-only (link) entry. Split number from the name.
            number, clean_title = parse_name(title)
            pid = "meta-" + uuid.uuid4().hex[:12]
            data["problems"][pid] = {
                "fileLess": True,
                "collection": collection,
                "topic": topic,
                "difficulty": difficulty,
                "number": number,
                "title": clean_title,
                "code": "",
                "tags": tags, "notes": notes, "link": link, "date": pdate,
            }
            save_data(data)
            return 200, {"ok": True, "id": pid}


def _identity_from_relpath(rel):
    """Derive (collection, topic, difficulty, filename-stem) from a scanned path."""
    parts = rel.split("/")
    collection = parts[0]
    topic = parts[1] if len(parts) >= 3 else "Misc"
    difficulty = "unknown"
    for p in parts[2:-1]:
        if p.lower() in FOLDER_TO_DIFF:
            difficulty = FOLDER_TO_DIFF[p.lower()]
            break
    stem = os.path.splitext(parts[-1])[0]
    return collection, topic, difficulty, stem


def _relpath_for(collection, topic, difficulty, title):
    ext = COLLECTIONS[collection]
    diff_folder = DIFF_TO_FOLDER.get(difficulty)
    parts = [REPO_ROOT, collection, _sanitize_filename(topic)]
    if diff_folder:
        parts.append(diff_folder)
    full = os.path.join(*parts, _sanitize_filename(title) + ext)
    return full, os.path.relpath(full, REPO_ROOT).replace(os.sep, "/")


def update_problem(body):
    pid = body.get("id")
    if not pid:
        return 400, {"error": "id required"}
    with _lock:
        data = load_data()
        entry = data["problems"].get(pid, {})
        file_less = entry.get("fileLess") or pid.startswith("meta-")

        if file_less:
            # Everything lives in data.json — just update the stored descriptor.
            for f in ("collection", "difficulty", "code", "tags", "notes", "link", "date"):
                if f in body:
                    entry[f] = body[f]
            if "topic" in body:
                entry["topic"] = (body["topic"] or "").strip()
            if "title" in body:
                number, clean = parse_name((body["title"] or "").strip())
                entry["number"] = number
                entry["title"] = clean
            data["problems"][pid] = entry
            save_data(data)
            return 200, {"ok": True, "id": pid}

        # File-backed problem. Identity fields may change -> move/rename the file.
        cc, ct, cd, cstem = _identity_from_relpath(pid)
        collection = body.get("collection") or cc
        if collection not in COLLECTIONS:
            return 400, {"error": "unknown collection"}
        topic = (body.get("topic") or ct).strip()
        difficulty = body.get("difficulty") or cd
        title = (body.get("title") or cstem).strip()

        full = os.path.join(REPO_ROOT, pid)
        new_full, new_rel = _relpath_for(collection, topic, difficulty, title)

        if new_rel != pid:
            if os.path.exists(new_full):
                return 409, {"error": f"target already exists: {new_rel}"}
            os.makedirs(os.path.dirname(new_full), exist_ok=True)
            if os.path.isfile(full):
                os.rename(full, new_full)
            entry = data["problems"].pop(pid, entry)
            pid, full = new_rel, new_full

        if "code" in body:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                code = body["code"]
                f.write(code if code.endswith("\n") else code + "\n")

        for f in ("tags", "notes", "link", "date"):
            if f in body:
                entry[f] = body[f]
        data["problems"][pid] = entry
        save_data(data)
        return 200, {"ok": True, "id": pid}


def add_tag(body):
    name = (body.get("name") or "").strip()
    color = body.get("color") or "#6b7280"
    if not name:
        return 400, {"error": "tag name required"}
    with _lock:
        data = load_data()
        if any(t["name"].lower() == name.lower() for t in data["tags"]):
            return 409, {"error": "tag already exists"}
        tag = {"id": "t-" + uuid.uuid4().hex[:10], "name": name, "color": color}
        data["tags"].append(tag)
        save_data(data)
        return 200, {"ok": True, "tag": tag}


def delete_tag(tag_id):
    with _lock:
        data = load_data()
        data["tags"] = [t for t in data["tags"] if t["id"] != tag_id]
        for m in data["problems"].values():
            if "tags" in m:
                m["tags"] = [t for t in m["tags"] if t != tag_id]
        save_data(data)
        return 200, {"ok": True}


def add_topic(body):
    collection = body.get("collection", "DSA")
    name = (body.get("name") or "").strip()
    if collection not in COLLECTIONS:
        return 400, {"error": "unknown collection"}
    if not name:
        return 400, {"error": "section name required"}
    with _lock:
        data = load_data()
        exists = any(t.get("collection") == collection and t.get("name") == name
                     for t in data["topics"])
        if not exists:
            data["topics"].append({"collection": collection, "name": name})
        save_data(data)
        # Create the folder so it's ready for the first problem.
        try:
            os.makedirs(os.path.join(REPO_ROOT, collection, _sanitize_filename(name)),
                        exist_ok=True)
        except OSError:
            pass
        return 200, {"ok": True}


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------
EXT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep the console quiet

    # -- helpers ----------------------------------------------------------
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def _serve_static(self, path):
        if path in ("", "/"):
            path = "/index.html"
        rel = path.lstrip("/")
        full = os.path.normpath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            self.send_error(404, "Not found")
            return
        ctype = EXT_TYPES.get(os.path.splitext(full)[1], "application/octet-stream")
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # -- verbs ------------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/data":
            try:
                self._send_json(200, build_model())
            except Exception as e:  # noqa: BLE001
                self._send_json(500, {"error": str(e)})
            return
        self._serve_static(parsed.path)

    def do_POST(self):
        parsed = urlparse(self.path)
        body = self._read_body()
        routes = {
            "/api/problem": add_problem,
            "/api/tag": add_tag,
            "/api/topic": add_topic,
        }
        fn = routes.get(parsed.path)
        if not fn:
            self._send_json(404, {"error": "unknown endpoint"})
            return
        try:
            status, payload = fn(body)
        except Exception as e:  # noqa: BLE001
            status, payload = 500, {"error": str(e)}
        self._send_json(status, payload)

    def do_PUT(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/problem":
            self._send_json(404, {"error": "unknown endpoint"})
            return
        try:
            status, payload = update_problem(self._read_body())
        except Exception as e:  # noqa: BLE001
            status, payload = 500, {"error": str(e)}
        self._send_json(status, payload)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == "/api/tag":
            tag_id = (qs.get("id") or [""])[0]
            status, payload = delete_tag(tag_id)
            self._send_json(status, payload)
            return
        self._send_json(404, {"error": "unknown endpoint"})


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print("LeetCode dashboard running")
    print(f"  Repo root : {REPO_ROOT}")
    print(f"  Open      : {url}")
    print("  Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
