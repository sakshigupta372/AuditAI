import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_broken_links(url, soup, max_links=50, timeout=5):
    """
    Checks for broken links on the page
    Returns dict with broken links, total links checked, and status
    """
    broken_links = []
    working_links = 0
    skipped_links = 0
    
    # Extract all links
    all_links = soup.find_all('a', href=True)
    links_to_check = []
    
    for link in all_links[:max_links]:  # Limit to avoid overwhelming
        href = link.get('href')
        
        # Skip anchors, mailto, tel, javascript
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
            skipped_links += 1
            continue
        
        # Convert relative URLs to absolute
        full_url = urljoin(url, href)
        
        # Only check HTTP/HTTPS
        if full_url.startswith(('http://', 'https://')):
            links_to_check.append((href, full_url))
    
    # Check links in parallel for speed
    def check_single_link(link_data):
        original_href, full_url = link_data
        try:
            response = requests.head(full_url, timeout=timeout, allow_redirects=True,
                                    headers={"User-Agent": "AI-Site-Auditor"})
            
            # If HEAD fails, try GET
            if response.status_code >= 400:
                response = requests.get(full_url, timeout=timeout, 
                                       headers={"User-Agent": "AI-Site-Auditor"})
            
            if response.status_code >= 400:
                return {'broken': True, 'url': original_href, 'status': response.status_code}
            else:
                return {'broken': False}
        except requests.exceptions.RequestException as e:
            return {'broken': True, 'url': original_href, 'status': 'Error', 'error': str(e)[:50]}
    
    # Use ThreadPoolExecutor for parallel checking
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_single_link, link): link for link in links_to_check}
        
        for future in as_completed(futures):
            result = future.result()
            if result['broken']:
                broken_links.append(result)
            else:
                working_links += 1
    
    total_checked = len(links_to_check)
    broken_count = len(broken_links)
    
    return {
        'total_links_checked': total_checked,
        'working_links': working_links,
        'broken_links_count': broken_count,
        'broken_links_details': broken_links[:10],  # Limit details to first 10
        'skipped_links': skipped_links,
        'link_health': 'Excellent' if broken_count == 0 else 'Good' if broken_count <= 2 else 'Needs Attention'
    }
