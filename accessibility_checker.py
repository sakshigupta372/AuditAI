from bs4 import BeautifulSoup

def check_accessibility(soup, url):
    """
    Checks WCAG 2.1 accessibility guidelines
    Returns dict with accessibility issues and score
    """
    issues = []
    score = 100
    
    # Check for missing alt text on images
    images = soup.find_all('img')
    images_without_alt = [img for img in images if not img.get('alt')]
    if images_without_alt:
        issues.append(f"❌ {len(images_without_alt)} images missing alt text")
        score -= min(20, len(images_without_alt) * 2)
    
    # Check for proper heading hierarchy
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    h1_count = len(soup.find_all('h1'))
    if h1_count == 0:
        issues.append("❌ No H1 heading found - important for screen readers")
        score -= 10
    elif h1_count > 1:
        issues.append(f"⚠️ Multiple H1 headings ({h1_count}) - should be unique")
        score -= 5
    
    # Check for form labels
    forms = soup.find_all('form')
    for form in forms:
        inputs = form.find_all(['input', 'select', 'textarea'])
        for input_elem in inputs:
            if input_elem.get('type') not in ['submit', 'button', 'hidden']:
                label_id = input_elem.get('id')
                if not label_id or not form.find('label', {'for': label_id}):
                    issues.append("❌ Form inputs missing associated labels")
                    score -= 5
                    break
    
    # Check for color contrast (basic check)
    inline_styles = soup.find_all(style=True)
    if inline_styles:
        issues.append("⚠️ Inline styles detected - may affect accessibility")
        score -= 3
    
    # Check for ARIA landmarks
    main_tag = soup.find('main')
    nav_tag = soup.find('nav')
    if not main_tag:
        issues.append("⚠️ No <main> landmark - helps screen reader navigation")
        score -= 5
    if not nav_tag:
        issues.append("⚠️ No <nav> landmark found")
        score -= 3
    
    # Check for link text
    links = soup.find_all('a')
    generic_link_text = ['click here', 'read more', 'here', 'link']
    for link in links:
        text = link.get_text().strip().lower()
        if text in generic_link_text:
            issues.append("❌ Generic link text found (e.g., 'click here') - use descriptive text")
            score -= 5
            break
    
    # Check for lang attribute
    html_tag = soup.find('html')
    if html_tag and not html_tag.get('lang'):
        issues.append("❌ Missing lang attribute on <html> tag")
        score -= 10
    
    # Check for skip links
    skip_link = soup.find('a', href='#main') or soup.find('a', href='#content')
    if not skip_link:
        issues.append("⚠️ No skip navigation link found")
        score -= 5
    
    # Check for video captions
    videos = soup.find_all('video')
    for video in videos:
        if not video.find('track', kind='captions'):
            issues.append("❌ Videos missing captions/subtitles")
            score -= 10
            break
    
    return {
        'accessibility_score': max(0, score),
        'accessibility_issues': issues if issues else ["✅ No major accessibility issues detected"],
        'wcag_compliance': 'Good' if score >= 80 else 'Needs Improvement' if score >= 60 else 'Poor'
    }
