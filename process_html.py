import os
import re

# List of files to process (excluding index.html initially to avoid double processing, but including it is fine too)
# Actually, I'll process everything to ensure consistency.

directory = '/Users/apple/Downloads/tpcschoolrr'

files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(directory, filename)
    print(f"Processing {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace protocol-relative URLs
    content = content.replace('="//', '="https://')
    content = content.replace('url("//', 'url("https://')
    
    # 2. Remove base tag
    content = re.sub(r'<base href="">', '<!-- <base href=""> -->', content)
    
    # 3. Fix internal links
    # Replace href="/" with href="index.html"
    content = content.replace('href="/"', 'href="index.html"')
    
    # Replace href="/<slug>" with href="<slug>.html"
    # We need to be careful not to replace external links or already fixed links
    # Regex look for href="/Something" where Something is not empty and doesn't contain . or /
    # actually, typical slugs are alphanumeric and hyphens.
    
    def replace_link(match):
        slug = match.group(1)
        return f'href="{slug}.html"'
    
    content = re.sub(r'href="/([a-zA-Z0-9-]+)"', replace_link, content)
    
    # Also fix data-href for mobile nav
    def replace_data_link(match):
        slug = match.group(1)
        return f'data-href="{slug}.html"'
        
    content = re.sub(r'data-href="/([a-zA-Z0-9-]+)"', replace_data_link, content)
    
    # Fix folder ids if necessary, usually they are just identifiers, but sometimes used for nav
    # data-folder-id="/about" -> data-folder-id="about" maybe? 
    # Let's inspect index.html again. 
    # <a data-folder-id="/about" href="/about">
    # If I change href to about.html, the data-folder-id might strictly be an ID.
    # I'll leave data-folder-id alone for now unless I see it breaking. 
    # Actually, previous grep showed: <button class="header-nav-folder-title" data-href="/about"
    # And <a data-folder-id="/about" href="/about">
    # So I should probably fix data-folder-id too if it's used for matching.
    
    def replace_folder_id(match):
        slug = match.group(1)
        return f'data-folder-id="{slug}.html"'
    content = re.sub(r'data-folder-id="/([a-zA-Z0-9-]+)"', replace_folder_id, content)

    # 4. Specific fixes for the known pages to ensure they link to each other correctly
    # The regex above should handle most, but let's be explicit for the known list if needed.
    # The regex `href="/([a-zA-Z0-9-]+)"` covers `href="/about"`, `href="/contact"`, etc.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Batch processing complete.")
