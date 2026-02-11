# 🧠 AuditAI — Enhanced Agentic AI Website Auditor (Gradio Edition)

An **Agentic AI-powered web application** built with **Gradio** that provides comprehensive website audits including **SEO, performance, accessibility, security, mobile responsiveness**, and **broken link detection** with **AI-generated insights and PDF reports**.

---

## 🆕 What's New in Gradio Edition

### **Enhanced Features:**
- ✅ **Accessibility Checker** - WCAG 2.1 compliance analysis
- ✅ **Mobile Responsiveness Analyzer** - Viewport, responsive images, touch targets
- ✅ **Broken Link Detection** - Parallel link checking with detailed reports
- ✅ **PDF Report Generation** - Professional downloadable audit reports
- ✅ **Historical Tracking** - Track score improvements over time
- ✅ **Trend Analysis** - Visualize performance changes across audits
- ✅ **Enhanced UI** - Modern Gradio tabbed interface with better UX

### **Original Features (Retained):**
- 🔍 Website scanning (load time, HTTPS, page size, links, headings)
- 🤖 Agentic AI analysis with Google Gemini 1.5 Flash
- 📊 Interactive visualizations (gauges, radar charts, bar charts)
- ⬇️ Downloadable optimized HTML
- 💡 AI-powered suggestions and fix snippets

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3️⃣ Run the Gradio App

```bash
python app_gradio.py
```

The app will launch at `http://localhost:7860` with a shareable link.

### 4️⃣ Run the Original Streamlit App (Optional)

```bash
streamlit run app.py
```

---

## 📋 New Features Details

### **♿ Accessibility Checker** (`accessibility_checker.py`)
Analyzes WCAG 2.1 compliance:
- Missing alt text on images
- Proper heading hierarchy (H1-H6)
- Form labels and ARIA landmarks
- Link text quality
- Language attributes
- Skip navigation links
- Video captions

### **📱 Mobile Responsiveness** (`mobile_checker.py`)
Checks mobile-friendliness:
- Viewport meta tag validation
- Responsive images (srcset/sizes)
- Page size optimization for mobile
- Flash content detection
- Fixed-width elements
- Touch target sizes
- Media queries analysis
- Relative font sizing

### **🔗 Broken Link Detector** (`link_checker.py`)
Identifies broken links:
- Parallel processing for speed (10 concurrent workers)
- Checks up to 50 links per audit
- HTTP status code validation
- Internal vs external link tracking
- Detailed error reporting

### **📄 PDF Report Generator** (`report_generator.py`)
Creates professional reports:
- Multi-page comprehensive audit summary
- Color-coded scores and metrics
- All detected issues organized by category
- AI recommendations
- Broken link details
- Timestamp and metadata

### **📈 Historical Tracking** (`history_tracker.py`)
Tracks performance over time:
- JSON-based storage (last 100 audits)
- Per-site history retrieval
- Trend data for visualizations
- Score comparison across audits

---

## 🎨 Gradio UI Structure

The new interface uses **5 tabs**:

1. **📊 Overview** - Summary, scores, gauge & radar charts
2. **📈 Metrics & Trends** - Technical metrics and historical trends
3. **⚠️ Issues** - AI, accessibility, mobile, and broken link issues
4. **✅ Recommendations** - AI-powered suggestions
5. **📄 PDF Report** - Download comprehensive report

---

## 📊 Scoring System

### **Overall Score Calculation** (0-100)
Based on:
- HTTPS (15 points)
- Load time (5-15 points)
- Title presence (10 points)
- Meta description (10 points)
- H1 tags (5-10 points)
- Images with alt text (up to 10 points)
- Links & scripts (up to 10 points)
- Paragraph content (up to 10 points)
- HTTP status (10 points)

### **Individual Scores**
- **SEO Score:** `100 - (images_without_alt × 5)`
- **Performance Score:** `100 - (load_time × 10)`
- **Accessibility Score:** WCAG compliance based (0-100)
- **Security Score:** 100 if HTTPS, else 50
- **Mobile Score:** Mobile-friendliness based (0-100)

---

## 🔧 Tech Stack

### **Core Technologies**
- **Python 3.9+**
- **Gradio 4.x** — Modern web UI framework
- **Google Gemini API** — Gemini 1.5 Flash for AI analysis
- **BeautifulSoup4** — HTML parsing
- **Requests** — HTTP client

### **Visualization & Reports**
- **Plotly** — Interactive charts (gauges, radar, bar)
- **Matplotlib** — Word clouds
- **Pandas** — Data manipulation
- **FPDF** — PDF generation

### **Other**
- **python-dotenv** — Environment variables
- **concurrent.futures** — Parallel link checking

---

## 📁 Project Structure

```
AuditAI-main/
├── app.py                      # Original Streamlit app
├── app_gradio.py               # NEW: Gradio app
├── scanner.py                  # Website scanner
├── ai_analyzer.py              # OpenAI integration
├── scoring.py                  # Score calculation
├── dashboard.py                # Streamlit dashboard
├── utils.py                    # Utility functions
├── accessibility_checker.py    # NEW: Accessibility analysis
├── mobile_checker.py           # NEW: Mobile responsiveness
├── link_checker.py             # NEW: Broken link detection
├── report_generator.py         # NEW: PDF generation
├── history_tracker.py          # NEW: Historical tracking
├── requirements.txt            # Dependencies
├── README.md                   # Original readme
├── README_GRADIO.md           # This file
└── .env                        # API keys (create this)
```

---

## 🎯 Usage Guide

1. **Enter URL:** Input the website URL (e.g., `https://example.com`)
2. **Choose Options:** Check/uncheck "Check for Broken Links" (optional, slower)
3. **Click Audit:** Start the comprehensive analysis
4. **View Results:** 
   - Overview tab shows summary and scores
   - Issues tab lists all detected problems
   - Recommendations tab shows AI suggestions
   - PDF tab provides downloadable report
5. **Track Progress:** Re-audit the same site to see trend improvements

---

## ⚡ Performance Notes

- **Broken Link Checking:** Uses parallel processing (10 workers) but can take 30-60s for 50 links
- **AI Analysis:** Powered by Google Gemini AI | Enhanced with Advanced Analytics
- **PDF Generation:** Instant (<1s)
- **Historical Trends:** Only show after 2+ audits of the same site

---

## 🔒 Environment Variables

Required in `.env` file:

```env
GEMINI_API_KEY=your-gemini-key-here
```

---

## 🆚 Gradio vs Streamlit

### **Why Gradio?**
- ✅ Easier deployment (built-in sharing)
- ✅ Better tab organization
- ✅ Cleaner API for complex workflows
- ✅ Automatic shareable links
- ✅ Better mobile experience

### **Keeping Streamlit?**
Both versions are maintained. Use:
- `app_gradio.py` for the enhanced version
- `app.py` for the original Streamlit version

---

## 👨‍💻 Author

**Mirza Yasir Abdullah Baig**

- 🌐 [Kaggle](https://www.kaggle.com/mirzayasirabdullah07)
- 💼 [LinkedIn](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/)
- 💻 [GitHub](https://github.com/mirzayasirabdullahbaig07)

---

## 📝 License

Educational purposes. Not for commercial use without permission.

---

## 🐛 Troubleshooting

**Issue:** Gemini API errors  
**Solution:** Check your API key in `.env` and get it from https://aistudio.google.com/app/apikey

**Issue:** Broken link checking takes too long  
**Solution:** Uncheck the "Check for Broken Links" option

**Issue:** PDF generation fails  
**Solution:** Ensure `fpdf` is installed: `pip install fpdf`

**Issue:** No trend data shown  
**Solution:** Audit the same site multiple times to build history

---

## 🚀 Future Enhancements

- [ ] Multi-page website crawling
- [ ] Competitor comparison
- [ ] Lighthouse integration
- [ ] Email report scheduling
- [ ] Database storage (replace JSON)
- [ ] Custom scoring weights
- [ ] Screenshot capture
- [ ] Security header analysis

---

## 📸 Screenshots

Coming soon! Run the app to see the beautiful new Gradio interface.

---

**Enjoy auditing! 🎉**
