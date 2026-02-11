from bs4 import BeautifulSoup

def check_mobile_responsiveness(soup, page_size_mb):
    """
    Checks mobile-friendliness and responsive design
    Returns dict with mobile issues and score
    """
    issues = []
    score = 100
    
    # Check viewport meta tag
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if not viewport:
        issues.append("❌ Missing viewport meta tag - critical for mobile devices")
        score -= 25
    else:
        content = viewport.get('content', '')
        if 'width=device-width' not in content:
            issues.append("⚠️ Viewport should include 'width=device-width'")
            score -= 10
        if 'initial-scale=1' not in content:
            issues.append("⚠️ Viewport should include 'initial-scale=1'")
            score -= 5
    
    # Check for responsive images
    images = soup.find_all('img')
    responsive_images = [img for img in images if img.get('srcset') or img.get('sizes')]
    if images and len(responsive_images) == 0:
        issues.append("⚠️ No responsive images detected (consider using srcset)")
        score -= 10
    
    # Check page size for mobile
    if page_size_mb > 3:
        issues.append(f"❌ Page size ({page_size_mb:.2f}MB) too large for mobile - should be <3MB")
        score -= 15
    elif page_size_mb > 1.5:
        issues.append(f"⚠️ Page size ({page_size_mb:.2f}MB) could be optimized for mobile")
        score -= 5
    
    # Check for mobile-unfriendly elements
    flash = soup.find_all(['embed', 'object'], type='application/x-shockwave-flash')
    if flash:
        issues.append("❌ Flash content detected - not supported on mobile devices")
        score -= 20
    
    # Check for fixed width elements
    tables = soup.find_all('table')
    for table in tables:
        if table.get('width') and 'px' in str(table.get('width')):
            issues.append("⚠️ Fixed-width tables detected - may not be mobile-friendly")
            score -= 5
            break
    
    # Check for touch-friendly elements
    buttons = soup.find_all('button')
    links = soup.find_all('a')
    small_touch_targets = 0
    for elem in buttons + links:
        style = elem.get('style', '')
        if 'font-size' in style and any(size in style for size in ['8px', '9px', '10px']):
            small_touch_targets += 1
    
    if small_touch_targets > 0:
        issues.append(f"⚠️ {small_touch_targets} elements may have small touch targets")
        score -= 10
    
    # Check for media queries in stylesheets
    styles = soup.find_all('style')
    links_css = soup.find_all('link', rel='stylesheet')
    has_media_queries = False
    for style in styles:
        if '@media' in style.get_text():
            has_media_queries = True
            break
    
    if not has_media_queries and len(styles) > 0:
        issues.append("⚠️ No media queries detected in inline styles")
        score -= 10
    
    # Check font sizes
    if not soup.find_all(style=lambda x: x and 'font-size' in x and any(unit in x for unit in ['em', 'rem', '%'])):
        issues.append("⚠️ Consider using relative font sizes (em, rem, %) for better mobile scaling")
        score -= 5
    
    return {
        'mobile_score': max(0, score),
        'mobile_issues': issues if issues else ["✅ Good mobile responsiveness"],
        'mobile_friendly': 'Yes' if score >= 80 else 'Partially' if score >= 60 else 'No'
    }
