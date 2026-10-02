/* ------------------------------------------------------------------ *
 * Qusay Coding Problems Dashboard — vanilla JS front end.
 * ------------------------------------------------------------------ */
"use strict";

const TAG_COLORS = [
  "#ef4444", "#f97316", "#eab308", "#22c55e", "#14b8a6",
  "#3b82f6", "#6366f1", "#a855f7", "#ec4899", "#78716c",
];

const DIFF_ORDER = ["easy", "medium", "hard", "unknown"];
const DIFF_LABEL = { easy: "Easy", medium: "Medium", hard: "Hard", unknown: "Other" };
const COLLECTION_LABEL = { DSA: "LeetCode", SQL: "SQL" };
const collLabel = (c) => COLLECTION_LABEL[c] || c;

const state = {
  problems: [],
  tags: [],
  topics: {},
  collections: ["DSA"],
  collection: null,            // active collection (LeetCode / SQL) — set on first load
  view: "topic",               // default landing view
  query: "",
  expandedTopics: new Set(),   // topic names currently expanded
  collapsedDiffs: new Set(),   // "topic::difficulty" keys the user has collapsed
};

// ---- tiny helpers ---------------------------------------------------
const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;");

const tagById = (id) => state.tags.find((t) => t.id === id);
const detailTitle = (p) => (p.number != null ? p.number + ". " : "") + p.title;

function chipStyle(color) {
  return `color:${color};background:color-mix(in srgb,${color} 14%,transparent);` +
         `border-color:color-mix(in srgb,${color} 30%,transparent);`;
}

function fmtDate(iso) {
  if (!iso) return "";
  const [y, m, d] = iso.split("-").map(Number);
  if (!y) return iso;
  return new Date(y, m - 1, d).toLocaleDateString(undefined,
    { year: "numeric", month: "short", day: "numeric" });
}

let toastTimer;
function toast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.hidden = true), 2200);
}

// ---- API ------------------------------------------------------------
const SERVER_DOWN_MSG =
  "Can't reach the dashboard server — is it still running? " +
  "Re-open start-dashboard.command, then try again.";

const api = {
  async load() {
    let r;
    try {
      r = await fetch("/api/data");
    } catch {
      throw new Error(SERVER_DOWN_MSG);
    }
    return r.json();
  },
  async send(method, path, body) {
    let r;
    try {
      r = await fetch(path, {
        method,
        headers: body ? { "Content-Type": "application/json" } : undefined,
        body: body ? JSON.stringify(body) : undefined,
      });
    } catch {
      // fetch() itself rejected -> the request never reached a live server
      // (e.g. the dashboard server was stopped). Give an actionable hint
      // instead of the browser's cryptic "Failed to fetch".
      throw new Error(SERVER_DOWN_MSG);
    }
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || `Request failed (${r.status})`);
    return j;
  },
};

async function refresh() {
  const data = await api.load();
  Object.assign(state, {
    problems: data.problems || [],
    tags: data.tags || [],
    topics: data.topics || {},
    collections: data.collections || ["DSA"],
  });
  if (!state.collection || !state.collections.includes(state.collection)) {
    state.collection = state.collections.includes("DSA") ? "DSA" : state.collections[0];
  }
  render();
}

// ---- matching / sorting --------------------------------------------
function matches(p, q) {
  if (!q) return true;
  const hay = [
    p.title, p.number, p.topic, p.difficulty, p.notes,
    ...(p.tags || []).map((id) => (tagById(id) || {}).name),
  ].join(" ").toLowerCase();
  return hay.includes(q);
}

function byRecency(a, b) {
  if (a.date && b.date) { if (a.date !== b.date) return a.date < b.date ? 1 : -1; }
  else if (a.date) return -1;
  else if (b.date) return 1;
  return (a.number || 1e9) - (b.number || 1e9) || a.title.localeCompare(b.title);
}
function byNumber(a, b) {
  return (a.number || 1e9) - (b.number || 1e9) || a.title.localeCompare(b.title);
}

// ---- collection tabs (LeetCode vs SQL) -----------------------------
function renderCollectionTabs() {
  const el = $("#collectionTabs");
  if (!el) return;
  el.innerHTML = state.collections.map((c) =>
    `<button class="seg ${c === state.collection ? "active" : ""}" data-coll="${esc(c)}">${esc(collLabel(c))}</button>`
  ).join("");
  el.querySelectorAll(".seg").forEach((b) =>
    b.addEventListener("click", () => {
      if (state.collection === b.dataset.coll) return;
      state.collection = b.dataset.coll;
      state.query = "";
      const search = $("#search");
      if (search) search.value = "";
      render();
    }));
}

// ---- rendering ------------------------------------------------------
function render() {
  renderCollectionTabs();
  const q = state.query.trim().toLowerCase();
  const inColl = state.problems.filter((p) => p.collection === state.collection);
  const list = inColl.filter((p) => matches(p, q));

  $("#countChip").textContent =
    `${inColl.length} solved` + (q ? ` · ${list.length} shown` : "");

  const content = $("#content");
  if (!list.length) {
    content.innerHTML = `<div class="empty">
      <p style="font-size:15px">${q ? "No problems match your search." : "Nothing here yet."}</p>
      <p>${q ? "" : "Click <strong>+ Add problem</strong> to get started."}</p></div>`;
    return;
  }

  if (state.view === "recency") {
    const rows = [...list].sort(byRecency).map(problemRow).join("");
    content.innerHTML = `<div class="card-list">${rows}</div>`;
    attachRowHandlers(content);
  } else {
    renderTopicView(content, list, q);
  }
}

function attachRowHandlers(root) {
  root.querySelectorAll(".prob").forEach((el) => {
    el.addEventListener("click", () => {
      const p = state.problems.find((x) => x.id === el.dataset.id);
      if (p) openDetail(p);
    });
  });
}

function renderTopicView(content, list, q) {
  const groups = {};
  for (const p of list) (groups[p.topic] ||= []).push(p);
  const names = Object.keys(groups).sort((a, b) => a.localeCompare(b));

  content.innerHTML = names.map((name) => {
    const probs = groups[name];
    const open = q ? true : state.expandedTopics.has(name);

    const byDiff = {};
    for (const p of probs) (byDiff[p.difficulty] ||= []).push(p);
    const diffs = DIFF_ORDER.filter((d) => byDiff[d]);

    const sub = open
      ? `${probs.length} problem${probs.length === 1 ? "" : "s"}`
      : diffs.map((d) => `${byDiff[d].length} ${DIFF_LABEL[d].toLowerCase()}`).join(" · ");

    let body = "";
    if (open) {
      body = `<div class="topic-card-body">` + diffs.map((d) => {
        const key = `${name}::${d}`;
        const dopen = q ? true : !state.collapsedDiffs.has(key);
        const rows = byDiff[d].sort(byNumber).map(problemRow).join("");
        return `<div class="diff-group">
          <button class="diff-group-head diff-${d}" data-diff="${esc(key)}">
            <span class="chevron ${dopen ? "open" : ""}">&#9654;</span>
            <span>${DIFF_LABEL[d]}</span>
            <span class="diff-group-count">${byDiff[d].length}</span>
          </button>
          ${dopen ? `<div class="diff-group-body">${rows}</div>` : ""}
        </div>`;
      }).join("") + `</div>`;
    }

    return `<div class="topic-card ${open ? "open" : ""}">
      <button class="topic-card-head" data-topic="${esc(name)}">
        <span class="chevron ${open ? "open" : ""}">&#9654;</span>
        <span class="topic-card-title">${esc(name)}</span>
        <span class="topic-card-sub">${esc(sub)}</span>
      </button>
      ${body}
    </div>`;
  }).join("");

  content.querySelectorAll(".topic-card-head").forEach((el) =>
    el.addEventListener("click", () => {
      const t = el.dataset.topic;
      state.expandedTopics.has(t) ? state.expandedTopics.delete(t) : state.expandedTopics.add(t);
      render();
    }));
  content.querySelectorAll(".diff-group-head").forEach((el) =>
    el.addEventListener("click", () => {
      const k = el.dataset.diff;
      state.collapsedDiffs.has(k) ? state.collapsedDiffs.delete(k) : state.collapsedDiffs.add(k);
      render();
    }));
  attachRowHandlers(content);
}

function problemRow(p) {
  const num = p.number != null ? `<span class="prob-num">${p.number}.</span>` : "";
  const chips = (p.tags || []).map((id) => {
    const t = tagById(id);
    return t ? `<span class="chip" style="${chipStyle(t.color)}">${esc(t.name)}</span>` : "";
  }).join("");
  const link = p.link ? `<span class="has-link">link ↗</span>` : "";
  return `<div class="prob" data-id="${esc(p.id)}">
    <div class="prob-main">
      <div class="prob-title">${num}<span class="prob-name">${esc(p.title)}</span></div>
      <div class="prob-meta">
        <span class="diff diff-${esc(p.difficulty)}">${esc(p.difficulty)}</span>
        <span class="chips">${chips}</span>
      </div>
    </div>
    <div class="prob-right">
      <span class="prob-date">${p.date ? fmtDate(p.date) : "—"}</span>
      ${link}
    </div>
  </div>`;
}

// ---- modal shell ----------------------------------------------------
function openModal(title, bodyHTML, opts = {}) {
  const bd = $("#modal");
  const m = bd.querySelector(".modal");
  bd.classList.toggle("full", !!opts.full);
  m.classList.toggle("full", !!opts.full);
  $("#modalTitle").textContent = title;
  $("#modalBody").innerHTML = bodyHTML;
  bd.hidden = false;
  return $("#modalBody");
}
function closeModal() {
  const bd = $("#modal");
  bd.hidden = true;
  bd.classList.remove("full");
  bd.querySelector(".modal").classList.remove("full");
  $("#modalBody").innerHTML = "";
}

// ---- minimal, safe markdown -> HTML --------------------------------
function mdInline(s) {
  return s
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*\n]+)\*/g, "<em>$1</em>")
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>');
}
function markdownToHtml(src) {
  const lines = esc(src).replace(/\r\n/g, "\n").split("\n");
  let html = "", inCode = false, inList = false;
  const codeBuf = [];
  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };
  for (const raw of lines) {
    if (/^```/.test(raw.trim())) {
      if (inCode) { html += `<pre><code>${codeBuf.join("\n")}</code></pre>`; codeBuf.length = 0; inCode = false; }
      else { closeList(); inCode = true; }
      continue;
    }
    if (inCode) { codeBuf.push(raw); continue; }
    const line = raw.trim();
    if (!line) { closeList(); continue; }
    let m;
    if ((m = line.match(/^(#{1,6})\s+(.*)$/))) {
      closeList();
      const lvl = Math.min(m[1].length, 3);
      html += `<h${lvl}>${mdInline(m[2])}</h${lvl}>`;
    } else if ((m = line.match(/^[-*]\s+(.*)$/))) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${mdInline(m[1])}</li>`;
    } else {
      closeList();
      html += `<p>${mdInline(line)}</p>`;
    }
  }
  closeList();
  if (inCode) html += `<pre><code>${codeBuf.join("\n")}</code></pre>`;
  return html;
}

// ---- tag picker (shared) -------------------------------------------
function tagPickerHTML(selected) {
  if (!state.tags.length) {
    return `<p class="hint">No tags yet. Create them under <strong>Tags</strong>.</p>`;
  }
  return `<div class="tag-pick">` + state.tags.map((t) =>
    `<span class="chip ${selected.has(t.id) ? "sel" : ""}" style="${chipStyle(t.color)}"
      data-tag="${t.id}">${esc(t.name)}</span>`).join("") + `</div>`;
}
function wireTagPicker(root, selected) {
  root.querySelectorAll(".tag-pick .chip").forEach((el) => {
    el.addEventListener("click", () => {
      const id = el.dataset.tag;
      if (selected.has(id)) { selected.delete(id); el.classList.remove("sel"); }
      else { selected.add(id); el.classList.add("sel"); }
    });
  });
}

const topicOptionsFor = (coll, selTopic) => {
  const list = (state.topics[coll] || []).slice();
  if (selTopic && !list.includes(selTopic)) list.push(selTopic);
  list.sort((a, b) => a.localeCompare(b));
  return list.map((t) => `<option ${t === selTopic ? "selected" : ""}>${esc(t)}</option>`).join("");
};

// ---- Add problem form ----------------------------------------------
function openProblemForm() {
  const selected = new Set();
  const today = new Date().toISOString().slice(0, 10);
  const defColl = state.collection || state.collections[0] || "DSA";
  const collOpts = state.collections.map((c) =>
    `<option value="${esc(c)}" ${c === defColl ? "selected" : ""}>${esc(collLabel(c))}</option>`).join("");

  const body = openModal("Add problem", `
    <form id="pform">
      <div class="row">
        <div class="field"><label>Collection</label>
          <select name="collection">${collOpts}</select></div>
        <div class="field"><label>Section / topic</label>
          <select name="topic" id="topicSel">${topicOptionsFor(defColl, null)}</select>
          <div class="hint">Add new ones via “Add section”.</div></div>
      </div>
      <div class="row">
        <div class="field"><label>Problem name</label>
          <input type="text" name="title" required placeholder="1. Two Sum">
          <div class="hint">Include the number, e.g. &ldquo;1. Two Sum&rdquo;.</div></div>
        <div class="field" style="flex:0 0 150px"><label>Difficulty</label>
          <select name="difficulty">
            ${["easy", "medium", "hard", "unknown"].map((d) =>
              `<option ${d === "easy" ? "selected" : ""}>${d}</option>`).join("")}
          </select></div>
      </div>

      <div class="field"><label>Solution</label>
        <div class="mode-toggle">
          <button type="button" class="seg active" data-mode="code">Paste code</button>
          <button type="button" class="seg" data-mode="link">Solution link</button>
        </div>
        <div data-pane="code">
          <textarea name="code" class="code" placeholder="class Solution: ..."></textarea>
          <div class="hint">If filled, a real file is written into your repo folders.</div>
        </div>
        <div data-pane="link" hidden>
          <input type="url" name="link" placeholder="https://leetcode.com/problems/...">
          <div class="hint">You can provide a link instead of code, or both.</div>
        </div>
      </div>

      <div class="field"><label>Tags</label>${tagPickerHTML(selected)}</div>

      <div class="field"><label>Notes / explanation</label>
        <textarea name="notes" placeholder="Approach, intuition, gotchas…"></textarea>
        <div class="hint">Markdown supported — headings (#), bold (**), lists (-), inline code and fenced code blocks.</div></div>

      <div class="field" style="max-width:200px"><label>Date solved</label>
        <input type="date" name="date" value="${today}"></div>

      <div class="form-actions">
        <button type="button" class="btn" id="cancelBtn">Cancel</button>
        <button type="submit" class="btn primary">Add problem</button>
      </div>
    </form>`);

  wireTagPicker(body, selected);

  body.querySelectorAll(".mode-toggle .seg").forEach((seg) => {
    seg.addEventListener("click", () => {
      body.querySelectorAll(".mode-toggle .seg").forEach((s) => s.classList.remove("active"));
      seg.classList.add("active");
      const mode = seg.dataset.mode;
      body.querySelector('[data-pane="code"]').hidden = mode !== "code";
      body.querySelector('[data-pane="link"]').hidden = mode !== "link";
    });
  });

  const collSel = body.querySelector('[name="collection"]');
  collSel.addEventListener("change", () => {
    body.querySelector("#topicSel").innerHTML = topicOptionsFor(collSel.value, null);
  });

  $("#cancelBtn").addEventListener("click", closeModal);
  $("#pform").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    const payload = {
      collection: f.collection.value,
      topic: f.topic.value,
      title: f.title.value.trim(),
      difficulty: f.difficulty.value,
      code: f.code.value,
      link: f.link.value.trim(),
      notes: f.notes.value,
      date: f.date.value || null,
      tags: [...selected],
    };
    try {
      if (!payload.topic) throw new Error("Pick or create a section first.");
      await api.send("POST", "/api/problem", payload);
      state.collection = payload.collection;   // jump to where it landed
      closeModal();
      await refresh();
      toast("Problem added");
    } catch (err) { toast(err.message); }
  });
}

// ---- Problem detail (view + inline edit on the SAME page) ----------
function openDetail(p) {
  openModal(detailTitle(p), "", { full: true });
  renderDetailView(p);
}

function renderDetailView(p) {
  $("#modalTitle").textContent = detailTitle(p);
  const chips = (p.tags || []).map((id) => {
    const t = tagById(id);
    return t ? `<span class="chip" style="${chipStyle(t.color)}">${esc(t.name)}</span>` : "";
  }).join("");

  $("#modalBody").innerHTML = `
    <div class="detail-page">
      <div class="detail-meta">
        <span class="diff diff-${esc(p.difficulty)}">${esc(p.difficulty)}</span>
        <span class="collection-tag">${esc(collLabel(p.collection))} · ${esc(p.topic)}</span>
        <span class="prob-date">${p.date ? fmtDate(p.date) : "no date"}</span>
        <span class="chips">${chips}</span>
        <span style="margin-left:auto"></span>
        ${p.code ? `<button class="btn small" id="copyBtn">Copy code</button>` : ""}
        <button class="btn small primary" id="editBtn">Edit</button>
      </div>
      ${p.link ? `<div class="detail-section detail-link"><h4>Link</h4>
        <a href="${esc(p.link)}" target="_blank" rel="noopener">${esc(p.link)}</a></div>` : ""}
      ${p.notes ? `<div class="detail-section"><h4>Notes</h4>
        <div class="md">${markdownToHtml(p.notes)}</div></div>` : ""}
      ${p.code ? `<div class="detail-section"><h4>Solution</h4>
        <pre class="code-block full">${esc(p.code)}</pre></div>`
        : (!p.link ? `<div class="detail-section muted">No code or link yet. Click Edit to add some.</div>` : "")}
    </div>`;

  const copyBtn = $("#copyBtn");
  if (copyBtn) copyBtn.addEventListener("click", () =>
    navigator.clipboard.writeText(p.code).then(() => toast("Copied")).catch(() => toast("Copy failed")));
  $("#editBtn").addEventListener("click", () => renderDetailEdit(p));
}

function renderDetailEdit(p) {
  $("#modalTitle").textContent = "Editing — " + detailTitle(p);
  const selected = new Set(p.tags || []);
  const titleVal = p.number != null ? p.number + ". " + (p.title || "") : (p.title || "");
  const collOpts = state.collections.map((c) =>
    `<option value="${esc(c)}" ${c === p.collection ? "selected" : ""}>${esc(collLabel(c))}</option>`).join("");

  $("#modalBody").innerHTML = `
    <div class="detail-page">
      <form id="editForm">
        <div class="detail-edit-actions">
          <span class="edit-flag">Editing</span>
          <span style="margin-left:auto"></span>
          <button type="button" class="btn small" id="cancelEdit">Cancel</button>
          <button type="submit" class="btn small primary">Save</button>
        </div>
        <div class="row">
          <div class="field"><label>Collection</label>
            <select name="collection">${collOpts}</select></div>
          <div class="field"><label>Section / topic</label>
            <select name="topic" id="editTopic">${topicOptionsFor(p.collection, p.topic)}</select></div>
          <div class="field" style="flex:0 0 140px"><label>Difficulty</label>
            <select name="difficulty">${DIFF_ORDER.map((d) =>
              `<option ${d === p.difficulty ? "selected" : ""}>${d}</option>`).join("")}</select></div>
        </div>
        <div class="row">
          <div class="field"><label>Problem name</label>
            <input type="text" name="title" required value="${esc(titleVal)}"></div>
          <div class="field" style="flex:0 0 190px"><label>Date solved</label>
            <input type="date" name="date" value="${p.date || ""}"></div>
        </div>
        <div class="field"><label>Solution link</label>
          <input type="url" name="link" value="${esc(p.link || "")}" placeholder="https://leetcode.com/problems/..."></div>
        <div class="field"><label>Tags</label>${tagPickerHTML(selected)}</div>
        <div class="field"><label>Notes / explanation</label>
          <textarea name="notes" class="notes-edit">${esc(p.notes || "")}</textarea>
          <div class="hint">Markdown supported — headings (#), bold (**), lists (-), inline code and fenced code blocks.</div></div>
        <div class="field"><label>Solution code</label>
          <textarea name="code" class="code code-edit" placeholder="class Solution: ...">${esc(p.code || "")}</textarea>
          ${p.hasFile ? `<div class="hint">Saved to <code>${esc(p.path)}</code> (renamed/moved if you change the name, section, difficulty or collection).</div>`
            : `<div class="hint">Add code to turn this into a real file in your repo.</div>`}</div>
      </form>
    </div>`;

  const body = $("#modalBody");
  wireTagPicker(body, selected);

  const collSel = body.querySelector('[name="collection"]');
  collSel.addEventListener("change", () => {
    body.querySelector("#editTopic").innerHTML = topicOptionsFor(collSel.value, null);
  });

  $("#cancelEdit").addEventListener("click", () => renderDetailView(p));
  $("#editForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    if (!f.title.value.trim()) return toast("Problem name is required");
    const payload = {
      id: p.id,
      collection: f.collection.value,
      topic: f.topic.value,
      difficulty: f.difficulty.value,
      title: f.title.value.trim(),
      link: f.link.value.trim(),
      notes: f.notes.value,
      date: f.date.value || null,
      code: f.code.value,
      tags: [...selected],
    };
    try {
      const j = await api.send("PUT", "/api/problem", payload);
      const newId = j.id || p.id;
      await refresh();
      const updated = state.problems.find((x) => x.id === newId);
      if (updated && updated.collection !== state.collection) {
        state.collection = updated.collection;
        render();
      }
      renderDetailView(updated || p);   // stay on this problem
      toast("Saved");
    } catch (err) { toast(err.message); }
  });
}

// ---- Manage tags ----------------------------------------------------
function openManageTags() {
  let pickedColor = TAG_COLORS[5];
  const render = () => {
    const rows = state.tags.length ? state.tags.map((t) =>
      `<div class="tag-manage-row">
        <span class="chip" style="${chipStyle(t.color)}">${esc(t.name)}</span>
        <span class="spacer"></span>
        <button class="btn small danger" data-del="${t.id}">Delete</button>
      </div>`).join("") : `<p class="hint">No tags yet.</p>`;

    const body = openModal("Tags", `
      <div class="field"><label>Your tags</label>${rows}</div>
      <div class="field"><label>New tag</label>
        <div class="row" style="align-items:flex-end">
          <input type="text" id="tagName" placeholder="e.g. Recursion" style="flex:1">
          <button class="btn primary" id="addTagBtn" style="flex:0 0 auto">Add tag</button>
        </div>
        <div class="color-swatches" id="swatches" style="margin-top:12px">
          ${TAG_COLORS.map((c) =>
            `<div class="swatch ${c === pickedColor ? "sel" : ""}" style="background:${c}" data-color="${c}"></div>`).join("")}
        </div>
      </div>`);

    body.querySelectorAll("[data-del]").forEach((b) =>
      b.addEventListener("click", async () => {
        try { await api.send("DELETE", `/api/tag?id=${encodeURIComponent(b.dataset.del)}`);
          await refresh(); render(); toast("Tag deleted"); }
        catch (e) { toast(e.message); }
      }));

    body.querySelectorAll(".swatch").forEach((s) =>
      s.addEventListener("click", () => {
        pickedColor = s.dataset.color;
        body.querySelectorAll(".swatch").forEach((x) => x.classList.remove("sel"));
        s.classList.add("sel");
      }));

    $("#addTagBtn").addEventListener("click", async () => {
      const name = $("#tagName").value.trim();
      if (!name) return toast("Enter a tag name");
      try { await api.send("POST", "/api/tag", { name, color: pickedColor });
        await refresh(); render(); toast("Tag created"); }
      catch (e) { toast(e.message); }
    });
  };
  render();
}

// ---- Add section ----------------------------------------------------
function openAddSection() {
  const defColl = state.collection || state.collections[0] || "DSA";
  const collOpts = state.collections.map((c) =>
    `<option value="${esc(c)}" ${c === defColl ? "selected" : ""}>${esc(collLabel(c))}</option>`).join("");
  openModal("Add section", `
    <form id="sform">
      <div class="field"><label>Collection</label><select name="collection">${collOpts}</select></div>
      <div class="field"><label>Section name</label>
        <input type="text" name="name" required placeholder="e.g. Backtracking">
        <div class="hint">Creates a new topic folder (e.g. <code>DSA/Backtracking/</code>).</div></div>
      <div class="form-actions">
        <button type="button" class="btn" id="cancelBtn">Cancel</button>
        <button type="submit" class="btn primary">Add section</button>
      </div>
    </form>`);
  $("#cancelBtn").addEventListener("click", closeModal);
  $("#sform").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await api.send("POST", "/api/topic",
        { collection: e.target.collection.value, name: e.target.name.value.trim() });
      state.collection = e.target.collection.value;
      closeModal(); await refresh(); toast("Section added");
    } catch (err) { toast(err.message); }
  });
}

// ---- wiring ---------------------------------------------------------
$("#search").addEventListener("input", (e) => { state.query = e.target.value; render(); });
document.querySelectorAll(".view-toggle .seg").forEach((seg) =>
  seg.addEventListener("click", () => {
    document.querySelectorAll(".view-toggle .seg").forEach((s) => s.classList.remove("active"));
    seg.classList.add("active");
    state.view = seg.dataset.view;
    render();
  }));
$("#addProblemBtn").addEventListener("click", openProblemForm);
$("#manageTagsBtn").addEventListener("click", openManageTags);
$("#addSectionBtn").addEventListener("click", openAddSection);
$("#modalClose").addEventListener("click", closeModal);
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") closeModal(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

refresh().catch((e) => toast("Failed to load: " + e.message));
