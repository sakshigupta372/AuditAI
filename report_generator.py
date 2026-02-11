from fpdf import FPDF
from datetime import datetime
import json

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'AuditAI - Website Audit Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(url, scan_data, ai_report, accessibility_data, mobile_data, link_data):
    """
    Generates a comprehensive PDF audit report
    Returns: PDF file path
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Website URL
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Website Analyzed:', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, url, 0, 1)
    pdf.ln(5)
    
    # Overall Scores Section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, 'Overall Performance Scores', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    scores = [
        ('Overall Score', scan_data.get('overall_score', 0)),
        ('SEO Score', scan_data.get('seo_score', 0)),
        ('Performance Score', scan_data.get('performance_score', 0)),
        ('Accessibility Score', accessibility_data.get('accessibility_score', 0)),
        ('Security Score', scan_data.get('security_score', 0)),
        ('Mobile Score', mobile_data.get('mobile_score', 0))
    ]
    
    for label, score in scores:
        color = (0, 200, 0) if score >= 80 else (255, 165, 0) if score >= 60 else (255, 0, 0)
        pdf.set_text_color(*color)
        pdf.cell(100, 8, f'{label}:', 0, 0)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, f'{score}/100', 0, 1)
        pdf.set_font('Arial', '', 11)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Technical Metrics
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, 'Technical Metrics', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    metrics = [
        ('Load Time', f"{scan_data.get('load_time', 0)} seconds"),
        ('Page Size', f"{scan_data.get('page_size_mb', 0):.2f} MB"),
        ('HTTPS Enabled', 'Yes' if scan_data.get('https') else 'No'),
        ('Status Code', str(scan_data.get('status_code', 'N/A'))),
        ('Total Links', str(scan_data.get('links_count', 0))),
        ('Internal Links', str(scan_data.get('internal_links', 0))),
        ('External Links', str(scan_data.get('external_links', 0))),
        ('Images without ALT', str(scan_data.get('images_without_alt', 0))),
        ('H1 Tags', str(scan_data.get('h1_count', 0))),
        ('Scripts', str(scan_data.get('scripts_count', 0)))
    ]
    
    for label, value in metrics:
        pdf.cell(95, 7, f'{label}:', 0, 0)
        pdf.cell(0, 7, value, 0, 1)
    
    pdf.ln(5)
    
    # Link Health
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, 'Link Health Check', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(95, 7, 'Total Links Checked:', 0, 0)
    pdf.cell(0, 7, str(link_data.get('total_links_checked', 0)), 0, 1)
    pdf.cell(95, 7, 'Working Links:', 0, 0)
    pdf.cell(0, 7, str(link_data.get('working_links', 0)), 0, 1)
    pdf.cell(95, 7, 'Broken Links:', 0, 0)
    pdf.set_text_color(255, 0, 0) if link_data.get('broken_links_count', 0) > 0 else pdf.set_text_color(0, 200, 0)
    pdf.cell(0, 7, str(link_data.get('broken_links_count', 0)), 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Broken Links Details
    if link_data.get('broken_links_details'):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Broken Links Found:', 0, 1)
        pdf.set_font('Arial', '', 9)
        for broken in link_data['broken_links_details'][:10]:
            pdf.multi_cell(0, 5, f"- {broken['url']} (Status: {broken['status']})")
        pdf.ln(3)
    
    # AI Detected Issues
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(255, 200, 200)
    pdf.cell(0, 10, 'AI Detected Issues', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    for issue in ai_report.get('issues', [])[:15]:
        pdf.multi_cell(0, 6, f'- {issue}')
    pdf.ln(5)
    
    # Accessibility Issues
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(255, 230, 200)
    pdf.cell(0, 10, 'Accessibility Issues', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    for issue in accessibility_data.get('accessibility_issues', [])[:15]:
        pdf.multi_cell(0, 6, f'{issue}')
    pdf.ln(5)
    
    # Mobile Issues
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(230, 200, 255)
    pdf.cell(0, 10, 'Mobile Responsiveness Issues', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    for issue in mobile_data.get('mobile_issues', [])[:15]:
        pdf.multi_cell(0, 6, f'{issue}')
    pdf.ln(5)
    
    # AI Suggestions
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_fill_color(200, 255, 200)
    pdf.cell(0, 10, 'AI Recommendations', 0, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    for suggestion in ai_report.get('suggestions', [])[:20]:
        pdf.multi_cell(0, 6, f'- {suggestion}')
    
    # Save PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audit_report_{timestamp}.pdf"
    pdf.output(filename)
    
    return filename
