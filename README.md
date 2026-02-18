---
title: Audit_AI
app_file: app_gradio.py
sdk: gradio
sdk_version: 5.47.2
---
# 🧠 AuditAI — AI Website Auditor

An **Agentic AI-powered web application** built with **Gradio** that audits any website and provides **SEO, performance, accessibility, and security insights**, along with **AI-generated fixes and optimized HTML**.


## 📌 Features

- 🔍 **Website Scanning**
  - Page load time
  - HTTPS detection
  - Page size analysis
  - Internal vs external links
  - Headings structure (H1, H2, H3)
  - Images without ALT attributes
  - Scripts, paragraphs, and links count

- 🤖 **Agentic AI Analysis**
  - Automatically detects website issues
  - Provides actionable AI-powered suggestions
  - Generates **HTML & SEO fix snippets**
  - Produces **fully optimized HTML**
  - Extracts top SEO keywords
  - Analyzes heading hierarchy

- 📊 **Interactive Dashboard**
  - Overall website score
  - SEO, Performance, Accessibility & Security scores
  - Gauge & radar charts
  - Bar charts & pie charts
  - Keyword word cloud
  - Heading hierarchy treemap
  - Page element heatmap

- ⬇️ **Download Optimized HTML**
  - One-click download of AI-improved webpage

---

## 🔍 Usage

1. Run the app locally using Gradio.
2. Enter a valid website URL.
3. Click **🚀 Start Audit**.
4. View:
   - ⚠️ Detected issues
   - ✅ AI-generated suggestions
   - 📊 Visual audit dashboard
   - 🤖 Agentic AI fixes
   - 📄 PDF Reports
5. Download the **optimized HTML** or **PDF report** if available.

---


---

## 📊 How It Works

1. The app scans the website using **BeautifulSoup & Requests**.
2. Raw metrics are calculated (SEO, performance, accessibility, mobile, security).
3. Scan data is sent to **Google Gemini** for agentic analysis.
4. AI returns:
   - Issues
   - Suggestions
   - Fix snippets
   - Optimized HTML
5. Results are visualized in a rich Gradio dashboard.

---

## ⚙️ Tech Stack

- **Python 3.9+**
- **Gradio** — Web UI
- **Google Gemini API** — Agentic AI analysis
- **BeautifulSoup** — HTML parsing
- **Requests** — Web scraping
- **Plotly & Matplotlib** — Interactive charts
- **WordCloud** — Keyword visualization
- **FPDF** — PDF report generation
- **dotenv** — Environment variables

---

---

## 👨‍💻 Author
**Sakshi Gupta**
