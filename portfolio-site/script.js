// Set to deployed RAG demo URL when available (Render/Railway)
// Local dev: http://127.0.0.1:8080
const RAG_DEMO_URL = "http://127.0.0.1:8080";

const projects = [
  {
    name: "Hybrid Knowledge Agent",
    tier: "Flagship",
    summary:
      "Multi-corpus RAG with domain routing across finance and nutrition knowledge bases. Hybrid BM25 + dense retrieval with citation-grounded streaming.",
    stack: ["FastAPI", "ChromaDB", "OpenAI", "BM25", "SSE"],
    complexity: 95,
    github: "https://github.com/Mahadmir45/ai-engineer-portfolio",
    askPrompt: "How does the hybrid RAG agent route queries between finance and nutrition domains?",
  },
  {
    name: "Food Search & Entity Matching",
    tier: "Tier 1",
    summary:
      "FastAPI + SQLite FTS search engine for glycemic index foods with USDA SR Legacy entity resolution and batch FDC ID mapping.",
    stack: ["FastAPI", "SQLite FTS", "Pandas", "Entity Resolution"],
    complexity: 82,
    github: "https://github.com/Mahadmir45",
    askPrompt: "How does the food search engine rank and match glycemic index foods to USDA entries?",
  },
  {
    name: "QuantFin Bayesian MMM",
    tier: "Tier 1",
    summary:
      "PyMC-based Marketing Mix Model with adstock, saturation curves, ROI uncertainty, and budget optimization for retail and luxury brands.",
    stack: ["PyMC", "Bayesian ML", "NumPy", "SLSQP"],
    complexity: 88,
    github: "https://github.com/Mahadmir45/QuantFin",
    askPrompt: "Explain the Bayesian MMM adstock and saturation architecture in QuantFin.",
  },
  {
    name: "Spectral Graph Engine",
    tier: "Tier 1",
    summary:
      "C++17 spectral graph compression pipeline for investor clustering and Max-Cut with LAPACK/CUDA and live benchmark dashboard.",
    stack: ["C++17", "LAPACK", "CUDA", "Graph ML"],
    complexity: 90,
    github: "https://github.com/Mahadmir45/mathematical-projects",
    askPrompt: "How does the spectral graph engine perform embedding and Max-Cut approximation?",
  },
  {
    name: "Supermarket Data Pipeline",
    tier: "Tier 2",
    summary:
      "Bilingual HK retail scraping (Wellcome, PNS, 7-Eleven) with OCR, master DB builder, and fuzzy USDA FDC matching at scale.",
    stack: ["Node.js", "RapidOCR", "thefuzz", "Databricks"],
    complexity: 78,
    github: "https://github.com/Mahadmir45",
    askPrompt: "Describe the supermarket data pipeline and USDA matching process.",
  },
  {
    name: "QuantFin Tableau Dashboards",
    tier: "Tier 2",
    summary:
      "Executive Tableau dashboards for equity markets, Topology Alpha strategy, and Bayesian MMM channel analytics.",
    stack: ["Tableau", "Python", "Prep Flows"],
    complexity: 70,
    github: "https://github.com/Mahadmir45/QuantFin-Tableau",
    askPrompt: "What visualizations does the QuantFin Tableau dashboard provide?",
  },
  {
    name: "Return Points Portal",
    tier: "Optional",
    summary:
      "Full-stack Next.js portal with Prisma, PostgreSQL, NextAuth, BullMQ, and cloud storage — production web engineering.",
    stack: ["Next.js 15", "TypeScript", "Prisma", "BullMQ"],
    complexity: 75,
    github: "https://github.com/Mahadmir45/hall3-return-points-portal",
    askPrompt: "What is the tech stack of the Return Points Portal?",
  },
];

const stats = [
  { value: "7", label: "Featured Projects" },
  { value: "2", label: "Knowledge Corpora" },
  { value: "100K+", label: "Scraped Records" },
  { value: "3", label: "Languages (Py/C++/TS)" },
];

const skills = [
  "RAG / LLM Systems",
  "Hybrid Retrieval (BM25 + Dense)",
  "PyMC / Bayesian ML",
  "Entity Resolution",
  "Graph Algorithms",
  "FastAPI",
  "ChromaDB / Vector Search",
  "Data Pipelines",
  "XGBoost / LSTM",
  "C++ Performance ML",
  "TypeScript / Next.js",
  "Streaming SSE APIs",
];

const suggestedPrompts = [
  "Explain your Bayesian MMM architecture",
  "How does food entity matching work?",
  "Compare spectral graph engine to standard clustering",
  "What is Topology Alpha in QuantFin?",
];

const archSteps = [
  "User Query",
  "Domain Router",
  "Hybrid Retriever",
  "BM25 + Dense RRF",
  "LLM Synthesis",
  "Cited Answer",
];

function renderStats() {
  const grid = document.getElementById("stats-grid");
  stats.forEach((item) => {
    const card = document.createElement("article");
    card.className = "stat-card";
    card.innerHTML = `<h3>${item.value}</h3><p>${item.label}</p>`;
    grid.appendChild(card);
  });
}

function renderArchitecture() {
  const flow = document.getElementById("arch-flow");
  archSteps.forEach((step, i) => {
    const el = document.createElement("div");
    el.className = "arch-step";
    el.textContent = step;
    flow.appendChild(el);
    if (i < archSteps.length - 1) {
      const arrow = document.createElement("span");
      arrow.className = "arch-arrow";
      arrow.textContent = "→";
      flow.appendChild(arrow);
    }
  });
}

function getRagUrl(prompt) {
  const base = RAG_DEMO_URL;
  if (prompt) {
    return `${base}?q=${encodeURIComponent(prompt)}`;
  }
  return base;
}

function renderProjects() {
  const grid = document.getElementById("project-grid");
  projects.forEach((project) => {
    const card = document.createElement("article");
    card.className = "project-card";
    const chips = project.stack.map((s) => `<span class="chip">${s}</span>`).join("");
    card.innerHTML = `
      <span class="tier">${project.tier}</span>
      <h3>${project.name}</h3>
      <p>${project.summary}</p>
      <div class="chip-list">${chips}</div>
      <div class="project-actions">
        <a class="button small ghost" href="${project.github}" target="_blank" rel="noreferrer">GitHub</a>
        <a class="button small" href="${getRagUrl(project.askPrompt)}" target="_blank" rel="noreferrer">Ask Agent</a>
      </div>
    `;
    grid.appendChild(card);
  });
}

function renderTags() {
  const cloud = document.getElementById("tag-cloud");
  skills.forEach((skill) => {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = skill;
    cloud.appendChild(tag);
  });
}

function renderComplexityChart() {
  const chart = document.getElementById("complexity-chart");
  const width = 800;
  const height = 360;
  const padding = 48;
  const displayProjects = projects.slice(0, 6);
  const maxValue = Math.max(...displayProjects.map((p) => p.complexity));
  const barWidth = 100;
  const gap = 20;

  const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  axis.setAttribute("x1", String(padding));
  axis.setAttribute("x2", String(width - padding));
  axis.setAttribute("y1", String(height - padding));
  axis.setAttribute("y2", String(height - padding));
  axis.setAttribute("stroke", "rgba(255,255,255,0.4)");
  chart.appendChild(axis);

  displayProjects.forEach((project, index) => {
    const x = padding + index * (barWidth + gap) + 8;
    const scaledHeight = (project.complexity / maxValue) * 220;
    const y = height - padding - scaledHeight;

    const bar = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    bar.setAttribute("x", String(x));
    bar.setAttribute("y", String(y));
    bar.setAttribute("width", String(barWidth));
    bar.setAttribute("height", String(scaledHeight));
    bar.setAttribute("rx", "10");
    bar.setAttribute("fill", "url(#bar-gradient)");
    bar.setAttribute("opacity", "0.95");
    chart.appendChild(bar);

    const value = document.createElementNS("http://www.w3.org/2000/svg", "text");
    value.setAttribute("x", String(x + barWidth / 2));
    value.setAttribute("y", String(y - 8));
    value.setAttribute("text-anchor", "middle");
    value.setAttribute("fill", "#dff7ff");
    value.setAttribute("font-size", "13");
    value.textContent = String(project.complexity);
    chart.appendChild(value);

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", String(x + barWidth / 2));
    label.setAttribute("y", String(height - 16));
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("fill", "#a9b5d4");
    label.setAttribute("font-size", "10");
    label.textContent = `P${index + 1}`;
    chart.appendChild(label);
  });

  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  defs.innerHTML = `
    <linearGradient id="bar-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6cb1ff"></stop>
      <stop offset="100%" stop-color="#4fe1b4"></stop>
    </linearGradient>
  `;
  chart.appendChild(defs);
}

function renderSkillRadar() {
  const canvas = document.getElementById("skill-canvas");
  const ctx = canvas.getContext("2d");
  const labels = ["RAG/LLM", "Bayesian ML", "Retrieval", "Graph ML", "Data Eng", "Full-Stack"];
  const values = [92, 88, 90, 85, 86, 78];
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = 145;
  const levels = 5;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "rgba(255,255,255,0.16)";
  ctx.lineWidth = 1;

  for (let level = 1; level <= levels; level += 1) {
    const r = (radius * level) / levels;
    ctx.beginPath();
    labels.forEach((_, i) => {
      const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.stroke();
  }

  labels.forEach((label, i) => {
    const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
    const x = centerX + Math.cos(angle) * (radius + 22);
    const y = centerY + Math.sin(angle) * (radius + 22);
    ctx.fillStyle = "#c4d1f0";
    ctx.font = "12px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(label, x, y);
  });

  ctx.beginPath();
  values.forEach((v, i) => {
    const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
    const r = (v / 100) * radius;
    const x = centerX + Math.cos(angle) * r;
    const y = centerY + Math.sin(angle) * r;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(89, 225, 194, 0.3)";
  ctx.strokeStyle = "#64ffd2";
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();
}

function renderSuggestedPrompts() {
  const container = document.getElementById("suggested-prompts");
  suggestedPrompts.forEach((prompt) => {
    const chip = document.createElement("button");
    chip.className = "prompt-chip";
    chip.textContent = prompt;
    chip.type = "button";
    chip.addEventListener("click", () => {
      window.open(getRagUrl(prompt), "_blank", "noreferrer");
    });
    container.appendChild(chip);
  });
}

function initRagEmbed() {
  const iframe = document.getElementById("rag-iframe");
  const fallback = document.getElementById("rag-fallback");
  const openBtn = document.getElementById("rag-open-btn");

  openBtn.href = RAG_DEMO_URL;

  // Try to load iframe if not localhost-only deployment
  if (RAG_DEMO_URL && !RAG_DEMO_URL.includes("127.0.0.1")) {
    iframe.src = RAG_DEMO_URL;
    iframe.classList.add("active");
    fallback.classList.add("hidden");
  }
}

renderStats();
renderArchitecture();
renderProjects();
renderTags();
renderComplexityChart();
renderSkillRadar();
renderSuggestedPrompts();
initRagEmbed();
