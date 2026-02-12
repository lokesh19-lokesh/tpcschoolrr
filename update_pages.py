#!/usr/bin/env python3
"""Script to add call button, floating WhatsApp, scroll-to-top, and external CSS to all pages."""
import re

PAGES = [
    "admissions.html",
    "contact.html", 
    "gallery.html",
    "ourcurriculum.html",
    "ourteam.html",
    "ourvalues.html",
    "parent-space.html",
    "why-rivo.html",
]

# CSS link to add in <head>
CSS_LINK = '<link href="css/floating-buttons.css" rel="stylesheet" type="text/css"/>'

# Call button HTML (desktop - with text)
CALL_BTN_DESKTOP = '''<a href="tel:+919111440044" class="navbar-call-btn" title="Call Us">
  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1.003 1.003 0 011.01-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.07 21 3 13.93 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.1.31.03.66-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-btn-text">+91 9111440044</span>
</a>'''

# Call button HTML (mobile - icon only via CSS)
CALL_BTN_MOBILE = '''<a href="tel:+919111440044" class="navbar-call-btn" title="Call Us">
  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1.003 1.003 0 011.01-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.07 21 3 13.93 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.1.31.03.66-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-btn-text">+91 9111440044</span>
</a>'''

# Floating call button HTML
FLOAT_CALL_BTN = '''<!-- Call Button (mobile only) -->
  <a href="tel:+919111440044" class="float-btn float-call-btn" title="Call Us">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1.003 1.003 0 011.01-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.07 21 3 13.93 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.1.31.03.66-.25 1.02l-2.2 2.2z"/></svg>
  </a>'''

# Floating buttons HTML
FLOATING_BUTTONS = '''
<!-- Floating Buttons -->
<div class="floating-buttons-container">
  ''' + FLOAT_CALL_BTN + '''
  <!-- WhatsApp Button -->
  <a href="https://wa.me/919111440044" target="_blank" rel="noopener noreferrer" class="float-btn whatsapp-btn" title="Chat on WhatsApp">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>
  <!-- Scroll to Top Button -->
  <button class="float-btn scroll-top-btn" title="Back to Top">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
  </button>
</div>
<script src="js/floating-buttons.js"></script>
'''

import os
BASE = "/Users/apple/Downloads/tpcschoolrr"

for page in PAGES:
    filepath = os.path.join(BASE, page)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add CSS link before </head> if not already there
    if 'floating-buttons.css' not in content:
        content = content.replace('</head>', CSS_LINK + '\n</head>')
    
    # 2. Add call button to DESKTOP header-actions (first occurrence)
    # The desktop section has `showOnMobile` then `showOnDesktop` divs
    # We need to add call button inside both showOnMobile and showOnDesktop
    # For the FIRST header-actions--right (desktop), replace empty showOnMobile/showOnDesktop
    
    # Find both header-actions--right blocks
    # Desktop block (first occurrence) - typically has empty showOnMobile/showOnDesktop
    desktop_pattern = re.compile(
        r'(<!-- Actions -->\s*\n\s*<div class="header-actions header-actions--right">\s*\n\s*<div class="showOnMobile">\s*\n\s*</div>\s*\n\s*<div class="showOnDesktop">\s*\n\s*</div>)',
        re.DOTALL
    )
    
    replacement_desktop = f'''<!-- Actions -->
<div class="header-actions header-actions--right">
<div class="showOnMobile">
{CALL_BTN_MOBILE}
</div>
<div class="showOnDesktop">
{CALL_BTN_DESKTOP}
</div>'''
    
    content = desktop_pattern.sub(replacement_desktop, content, count=1)
    
    # 3. For the MOBILE header-actions--right (second occurrence)
    # It has cart items inside showOnMobile/showOnDesktop - just add call button before the cart
    # Add call button to the mobile section's showOnMobile div
    # Pattern: find second header-actions--right > showOnMobile > content
    # Instead of complex regex, let's find the mobile section by looking for header-display-mobile
    
    # Hide cart in mobile section and add call button
    if 'header-actions-action--cart' in content:
        # Add CSS to hide cart on mobile
        if '.showOnMobile .header-actions-action--cart' not in content:
            content = content.replace(
                '<style id="custom-navbar-style">',
                '<style id="custom-navbar-style">\n    .showOnMobile .header-actions-action--cart { display: none !important; }'
            )
    
    # 4. Add floating buttons before </body> if not already there
    if 'floating-buttons-container' not in content:
        content = content.replace('</body>', FLOATING_BUTTONS + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {page}")

print("\nDone! All pages updated.")
