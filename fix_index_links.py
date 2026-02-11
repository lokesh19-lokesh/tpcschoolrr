import re

filepath = '/Users/apple/Downloads/tpcschoolrr/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Map of Link Text -> Filename
link_map = {
    'Mission & Values': 'mission-values.html',
    'Our Story': 'ourstory.html',
    'Giving Back': 'savanna-gives-back.html',
    'FAQs': 'faqs.html',
    'Careers': 'educator.html',
    'Contact Us': 'contact.html',
    'Our Approach': 'our-approach.html',
    'Enrollment & Tuition': 'enrollment.html',
    'Infant \(3M-24M\)': 'infant.html',
    'Toddler \(2Y-3Y\)': 'toddler.html',
    'Nursery School \(3Y-5Y\)': 'nursery.html',
    'After School Enrichment': 'preschool-1.html',
    'Employer Partnerships': 'employer.html',
    'Colima Orphanage': 'new-page-2.html',
    'Savanna Near You': 'savanna-near-you.html',
    'Shop': 'shop.html'
}

# 1. Fix standard nav links
# Pattern: <a href="..."> ... <span ...>Link Text</span> ... </a>
# We look for the span text and replace the closest preceding href.

for text, filename in link_map.items():
    # Regex to capture the href quote char, usage: href="[^"]*" ... text
    # We want to replace the href value.
    # Because valid HTML can vary, we'll try to capture the whole tag structure.
    # Note: text might have newlines or spaces around it in the file.
    
    # Strategy: Find the text, look backwards for the nearest href.
    # This is tricky with regex. 
    # Alternative: Use simple replacement of known chunks if possible, but context varies (desktop/mobile).
    
    # Let's try a regex that matches the whole anchor tag if possible, or close enough.
    # <a href="about.html">\s*<span[^>]*>\s*Mission & Values
    
    pattern = r'(<a\s+href=")[^"]*("\s*>\s*<span[^>]*>\s*' + text + r')'
    replacement = r'\1' + filename + r'\2'
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Also handle the Top Level Collections which might not have the span class "header-nav-folder-item-content"
    # e.g. <a href="about.html" data-animation-role="header-element">\s*Employer Partnerships
    pattern_collection = r'(<a\s+href=")[^"]*("\s+data-animation-role="header-element">\s*' + text + r')'
    replacement_collection = r'\1' + filename + r'\2'
    content = re.sub(pattern_collection, replacement_collection, content, flags=re.IGNORECASE)

    # Handle Mobile Menu Items
    # <a href="about.html">\s*<div class="header-menu-nav-item-content">\s*Mission & Values
    pattern_mobile = r'(<a\s+href=")[^"]*("\s*>\s*<div class="header-menu-nav-item-content">\s*' + text + r')'
    content = re.sub(pattern_mobile, replacement, content, flags=re.IGNORECASE)

# 2. Fix specific Folder Buttons (About, School) to be placeholders #
# Currently they are "about.html" due to my error.
# <button class="header-nav-folder-title" data-href="about.html"
# Text: About
# Text: School & Tuition

content = re.sub(r'(data-href=")[^"]*("\s*data-animation-role="header-element"[^>]*>\s*<span[^>]*>\s*About)', r'\1#\2', content)
content = re.sub(r'(data-href=")[^"]*("\s*data-animation-role="header-element"[^>]*>\s*<span[^>]*>\s*School & Tuition)', r'\1#\2', content)

# 3. Fix Folder Back buttons and active states in mobile menu if needed.
# <a data-folder-id="#" href="about.html"> ... About
# <a data-folder-id="#" href="about.html"> ... School & Tuition
# These should probably be # for the href.

content = re.sub(r'(<a\s+data-folder-id="#"\s+href=")[^"]*("\s*>\s*<div[^>]*>\s*<span[^>]*>Folder:</span>\s*<span[^>]*>About)', r'\1#\2', content)
content = re.sub(r'(<a\s+data-folder-id="#"\s+href=")[^"]*("\s*>\s*<div[^>]*>\s*<span[^>]*>Folder:</span>\s*<span[^>]*>School & Tuition)', r'\1#\2', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Index links fixed.")
