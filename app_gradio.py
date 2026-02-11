import gradio as gr
from scanner import scan_website
from ai_analyzer import analyze_with_ai
from utils import normalize_url, is_valid_url
from scoring import calculate_score
from accessibility_checker import check_accessibility
from mobile_checker import check_mobile_responsiveness
from link_checker import check_broken_links
from report_generator import generate_pdf_report
from history_tracker import save_audit, get_trend_data
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from bs4 import BeautifulSoup
import requests

def create_gauge_chart(score, title):
    """Create a gauge chart for scores"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightcoral"},
                {'range': [50, 80], 'color': "lightyellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_radar_chart(scores_dict):
    """Create radar chart for all scores"""
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Audit Scores'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        title="Overall Website Health Radar",
        height=400
    )
    return fig

def create_metrics_bar_chart(scan_data):
    """Create bar chart for SEO metrics"""
    metrics_data = pd.DataFrame({
        'Metric': ['H1 Tags', 'H2 Tags', 'H3 Tags', 'Images w/o ALT', 'Links', 'Scripts'],
        'Value': [
            scan_data.get('h1_count', 0),
            scan_data.get('h2_count', 0),
            scan_data.get('h3_count', 0),
            scan_data.get('images_without_alt', 0),
            scan_data.get('links_count', 0),
            scan_data.get('scripts_count', 0)
        ]
    })
    
    fig = px.bar(metrics_data, x='Metric', y='Value', 
                 title='SEO & Technical Metrics',
                 color='Value',
                 color_continuous_scale='Viridis')
    fig.update_layout(height=400)
    return fig

def create_trend_chart(url):
    """Create trend chart from history"""
    trend_data = get_trend_data(url)
    
    if not trend_data:
        return None
    
    df = pd.DataFrame(trend_data['scores'])
    df['Date'] = trend_data['dates']
    
    fig = go.Figure()
    for col in df.columns[:-1]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[col], mode='lines+markers', name=col))
    
    fig.update_layout(
        title='Score Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Score',
        height=400
    )
    return fig

def audit_website(url, check_links=True):
    """Main audit function"""
    if not url or not is_valid_url(url):
        return ("❌ Invalid URL", None, None, None, None, None, None, None, None, None, None)
    
    url = normalize_url(url)
    status_msg = f"🔍 Scanning {url}..."
    
    # Step 1: Scan website
    scan_data = scan_website(url)
    
    if "error" in scan_data:
        return (f"❌ Error: {scan_data['error']}", None, None, None, None, None, None, None, None, None, None)
    
    # Step 2: Get page content for additional checks
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "AI-Site-Auditor"})
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        return ("❌ Failed to fetch page content", None, None, None, None, None, None, None, None, None, None)
    
    # Step 3: Run all checks
    accessibility_data = check_accessibility(soup, url)
    mobile_data = check_mobile_responsiveness(soup, scan_data.get('page_size_mb', 0))
    
    if check_links:
        link_data = check_broken_links(url, soup, max_links=50)
    else:
        link_data = {'total_links_checked': 0, 'working_links': 0, 'broken_links_count': 0, 
                     'broken_links_details': [], 'link_health': 'Skipped'}
    
    # Step 4: Calculate scores
    overall_score = calculate_score(scan_data)
    scan_data["overall_score"] = overall_score
    scan_data["seo_score"] = max(0, 100 - scan_data.get("images_without_alt", 0) * 5)
    scan_data["performance_score"] = max(0, 100 - scan_data.get("load_time", 5) * 10)
    scan_data["security_score"] = 100 if scan_data.get("https") else 50
    
    # Step 5: AI Analysis
    ai_report = analyze_with_ai(scan_data)
    
    # Step 6: Save to history
    save_audit(url, scan_data, ai_report, accessibility_data, mobile_data, link_data)
    
    # Step 7: Create visualizations
    scores_dict = {
        'SEO': scan_data["seo_score"],
        'Performance': scan_data["performance_score"],
        'Accessibility': accessibility_data['accessibility_score'],
        'Security': scan_data["security_score"],
        'Mobile': mobile_data['mobile_score']
    }
    
    gauge_overall = create_gauge_chart(overall_score, "Overall Score")
    radar_chart = create_radar_chart(scores_dict)
    metrics_chart = create_metrics_bar_chart(scan_data)
    trend_chart = create_trend_chart(url)
    
    # Step 8: Format results
    summary = f"""
# 🎯 Audit Summary for {url}

## 📊 Scores
- **Overall Score:** {overall_score}/100
- **SEO Score:** {scan_data['seo_score']}/100
- **Performance Score:** {scan_data['performance_score']}/100
- **Accessibility Score:** {accessibility_data['accessibility_score']}/100
- **Security Score:** {scan_data['security_score']}/100
- **Mobile Score:** {mobile_data['mobile_score']}/100

## 🔧 Technical Metrics
- **Load Time:** {scan_data.get('load_time', 0)}s
- **Page Size:** {scan_data.get('page_size_mb', 0):.2f} MB
- **HTTPS:** {'✅ Yes' if scan_data.get('https') else '❌ No'}
- **Status Code:** {scan_data.get('status_code', 'N/A')}

## 🔗 Link Health
- **Total Links Checked:** {link_data['total_links_checked']}
- **Working Links:** {link_data['working_links']}
- **Broken Links:** {link_data['broken_links_count']}
- **Health Status:** {link_data['link_health']}

## 📱 Mobile Friendliness
- **Status:** {mobile_data['mobile_friendly']}

## ♿ Accessibility
- **WCAG Compliance:** {accessibility_data['wcag_compliance']}
"""
    
    # Format AI Issues
    ai_issues_text = "## ⚠️ AI Detected Issues\n\n"
    for issue in ai_report.get('issues', [])[:10]:
        ai_issues_text += f"- {issue}\n"
    
    # Format AI Suggestions
    ai_suggestions_text = "## ✅ AI Recommendations\n\n"
    for suggestion in ai_report.get('suggestions', [])[:10]:
        ai_suggestions_text += f"- {suggestion}\n"
    
    # Format Accessibility Issues
    accessibility_text = "## ♿ Accessibility Issues\n\n"
    for issue in accessibility_data.get('accessibility_issues', []):
        accessibility_text += f"{issue}\n\n"
    
    # Format Mobile Issues
    mobile_text = "## 📱 Mobile Issues\n\n"
    for issue in mobile_data.get('mobile_issues', []):
        mobile_text += f"{issue}\n\n"
    
    # Format Broken Links
    broken_links_text = "## 🔗 Broken Links Details\n\n"
    if link_data['broken_links_details']:
        for broken in link_data['broken_links_details']:
            broken_links_text += f"- **URL:** {broken['url']}\n"
            broken_links_text += f"  **Status:** {broken['status']}\n\n"
    else:
        broken_links_text += "✅ No broken links detected!\n"
    
    # Generate PDF
    try:
        pdf_path = generate_pdf_report(url, scan_data, ai_report, accessibility_data, mobile_data, link_data)
    except:
        pdf_path = None
    
    return (
        summary,
        ai_issues_text,
        ai_suggestions_text,
        accessibility_text,
        mobile_text,
        broken_links_text,
        gauge_overall,
        radar_chart,
        metrics_chart,
        trend_chart if trend_chart else None,
        pdf_path
    )

# Create Gradio Interface
with gr.Blocks(title="AuditAI - Agentic Website Auditor", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🧠 AuditAI - Agentic AI Website Auditor
    **Powered by Google Gemini 1.5 Flash | Enhanced with Advanced Analytics**
    
    Comprehensive website auditing with SEO, Performance, Accessibility, Security, and Mobile analysis.
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            url_input = gr.Textbox(
                label="Website URL",
                placeholder="https://example.com",
                info="Enter the full URL of the website to audit"
            )
        with gr.Column(scale=1):
            check_links_checkbox = gr.Checkbox(
                label="Check for Broken Links",
                value=True,
                info="May take longer"
            )
    
    audit_btn = gr.Button("🚀 Start Audit", variant="primary", size="lg")
    
    with gr.Tabs():
        with gr.Tab("📊 Overview"):
            summary_output = gr.Markdown(label="Audit Summary")
            
            with gr.Row():
                gauge_plot = gr.Plot(label="Overall Score")
                radar_plot = gr.Plot(label="Health Radar")
        
        with gr.Tab("📈 Metrics & Trends"):
            metrics_plot = gr.Plot(label="Technical Metrics")
            trend_plot = gr.Plot(label="Historical Trends")
        
        with gr.Tab("⚠️ Issues"):
            ai_issues_output = gr.Markdown(label="AI Detected Issues")
            accessibility_output = gr.Markdown(label="Accessibility Issues")
            mobile_output = gr.Markdown(label="Mobile Issues")
            broken_links_output = gr.Markdown(label="Broken Links")
        
        with gr.Tab("✅ Recommendations"):
            ai_suggestions_output = gr.Markdown(label="AI Recommendations")
        
        with gr.Tab("📄 PDF Report"):
            gr.Markdown("### Download your comprehensive audit report")
            pdf_output = gr.File(label="Download PDF Report")
    
    # Event handler
    audit_btn.click(
        fn=audit_website,
        inputs=[url_input, check_links_checkbox],
        outputs=[
            summary_output,
            ai_issues_output,
            ai_suggestions_output,
            accessibility_output,
            mobile_output,
            broken_links_output,
            gauge_plot,
            radar_plot,
            metrics_plot,
            trend_plot,
            pdf_output
        ]
    )
    
    gr.Markdown("""
    ---
    ### 👨‍💻 Built by Mirza Yasir Abdullah Baig
    **Connect:** [LinkedIn](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/) | 
    [GitHub](https://github.com/mirzayasirabdullahbaig07) | 
    [Kaggle](https://www.kaggle.com/mirzayasirabdullah07)
    
    **Features:** SEO Analysis • Performance Metrics • Accessibility Check • Broken Link Detection • 
    Mobile Responsiveness • AI-Powered Insights • PDF Reports • Historical Tracking
    """)

if __name__ == "__main__":
    demo.launch(share=True)
