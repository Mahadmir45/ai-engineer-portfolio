const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const corpusStats = document.getElementById("corpus-stats");
const suggestions = document.getElementById("suggestions");

function routeBadgeClass(route) {
  if (route === "finance") return "finance";
  if (route === "nutrition") return "nutrition";
  return "both";
}

function routeLabel(route) {
  if (route === "finance") return "Finance KB";
  if (route === "nutrition") return "Nutrition KB";
  return "Both Corpora";
}

async function loadCorpusStats() {
  try {
    const res = await fetch("/api/corpus-stats");
    const data = await res.json();
    const total = Object.values(data).reduce((a, b) => a + b, 0);
    corpusStats.textContent = `${total} chunks indexed · Finance: ${data.finance_kb || 0} · Nutrition: ${data.nutrition_kb || 0}`;
  } catch {
    corpusStats.textContent = "Corpus not indexed — run ingestion/build_index.py";
  }
}

function appendUserMessage(text) {
  const el = document.createElement("div");
  el.className = "message user";
  el.textContent = text;
  chatLog.appendChild(el);
  chatLog.scrollTop = chatLog.scrollHeight;
  return el;
}

function createAssistantMessage() {
  const el = document.createElement("div");
  el.className = "message assistant";
  el.innerHTML = `<div class="message-meta"><span class="badge">...</span></div><div class="content"><span class="typing">Retrieving...</span></div>`;
  chatLog.appendChild(el);
  chatLog.scrollTop = chatLog.scrollHeight;
  return el;
}

function renderCitations(sources) {
  if (!sources || sources.length === 0) return "";
  const items = sources
    .map(
      (s, i) =>
        `<div class="citation-item"><strong>[${i + 1}] ${s.project}</strong> (${s.title}) — score ${s.score}<br>${escapeHtml(s.snippet)}</div>`
    )
    .join("");
  return `<details class="citations" open><summary>${sources.length} source(s)</summary>${items}</details>`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function sendMessage(text) {
  const query = text.trim();
  if (!query) return;

  appendUserMessage(query);
  chatInput.value = "";
  sendBtn.disabled = true;

  const assistantEl = createAssistantMessage();
  const metaEl = assistantEl.querySelector(".message-meta");
  const contentEl = assistantEl.querySelector(".content");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query }),
    });

    if (!res.ok) {
      contentEl.textContent = `Error: ${res.status} ${res.statusText}`;
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let fullText = "";
    let sources = [];
    let route = "both";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const jsonStr = line.slice(6);
        try {
          const data = JSON.parse(jsonStr);
          if (data.type === "meta") {
            route = data.route;
            sources = data.sources || [];
            metaEl.innerHTML = `<span class="badge ${routeBadgeClass(route)}">${routeLabel(route)}</span>`;
            contentEl.innerHTML = "";
          } else if (data.type === "token") {
            fullText += data.content;
            contentEl.textContent = fullText;
            chatLog.scrollTop = chatLog.scrollHeight;
          } else if (data.type === "done") {
            contentEl.insertAdjacentHTML("beforeend", renderCitations(sources));
          }
        } catch {
          // skip malformed SSE lines
        }
      }
    }
  } catch (err) {
    contentEl.textContent = `Network error: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(chatInput.value);
});

suggestions.addEventListener("click", (e) => {
  const btn = e.target.closest(".suggestion");
  if (btn) sendMessage(btn.dataset.q);
});

// Pre-fill from URL ?q= parameter
const params = new URLSearchParams(window.location.search);
const prefill = params.get("q");
if (prefill) {
  chatInput.value = prefill;
  sendMessage(prefill);
}

loadCorpusStats();
chatInput.focus();
