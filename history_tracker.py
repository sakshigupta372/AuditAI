import json
import os
from datetime import datetime

HISTORY_FILE = "audit_history.json"

def load_history():
    """Load audit history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_audit(url, scan_data, ai_report, accessibility_data, mobile_data, link_data):
    """Save current audit to history"""
    history = load_history()
    
    audit_entry = {
        'timestamp': datetime.now().isoformat(),
        'url': url,
        'overall_score': scan_data.get('overall_score', 0),
        'seo_score': scan_data.get('seo_score', 0),
        'performance_score': scan_data.get('performance_score', 0),
        'accessibility_score': accessibility_data.get('accessibility_score', 0),
        'security_score': scan_data.get('security_score', 0),
        'mobile_score': mobile_data.get('mobile_score', 0),
        'load_time': scan_data.get('load_time', 0),
        'page_size_mb': scan_data.get('page_size_mb', 0),
        'broken_links': link_data.get('broken_links_count', 0),
        'https': scan_data.get('https', False)
    }
    
    history.append(audit_entry)
    
    # Keep only last 100 audits
    history = history[-100:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
    
    return audit_entry

def get_site_history(url, limit=10):
    """Get history for a specific site"""
    history = load_history()
    site_history = [entry for entry in history if entry['url'] == url]
    return site_history[-limit:]

def get_trend_data(url):
    """Get trend data for charts"""
    site_history = get_site_history(url, limit=20)
    
    if not site_history:
        return None
    
    dates = [entry['timestamp'][:10] for entry in site_history]
    scores = {
        'Overall': [entry['overall_score'] for entry in site_history],
        'SEO': [entry['seo_score'] for entry in site_history],
        'Performance': [entry['performance_score'] for entry in site_history],
        'Accessibility': [entry['accessibility_score'] for entry in site_history],
        'Security': [entry['security_score'] for entry in site_history],
        'Mobile': [entry['mobile_score'] for entry in site_history]
    }
    
    return {'dates': dates, 'scores': scores}
