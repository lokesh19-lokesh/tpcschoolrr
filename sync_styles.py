import os
import re
from bs4 import BeautifulSoup

# Configuration
BASE_DIR = '/Users/apple/Downloads/tpcschoolrr'
SOURCE_FILE = 'index.html'
CSS_DIR = 'css'

def get_local_css_links(soup):
    """Extracts <link> tags pointing to local CSS files."""
    links = []
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if href.startswith('css/') or (not href.startswith('http') and not href.startswith('//')):
             # It's likely local. We want to capture the whole tag or reconstruct it.
             # We'll just construct a string for it to ensure consistency
             links.append(str(link))
    return links

def get_header(soup):
    """Extracts the header element."""
    header = soup.find('header', id='header')
    return str(header) if header else None

def sync_styles():
    source_path = os.path.join(BASE_DIR, SOURCE_FILE)
    
    if not os.path.exists(source_path):
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    print(f"Reading source configuration from {SOURCE_FILE}...")
    with open(source_path, 'r', encoding='utf-8') as f:
        source_soup = BeautifulSoup(f, 'html.parser')

    local_css_tags = get_local_css_links(source_soup)
    header_content = get_header(source_soup)
    
    if not header_content:
        print("Error: Could not find header in source file.")
        return

    # Files to process
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html') and f != SOURCE_FILE]
    
    for filename in files:
        filepath = os.path.join(BASE_DIR, filename)
        print(f"Processing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            target_soup = BeautifulSoup(f, 'html.parser')
            
        # 1. Update CSS
        # Remove existing remote CSS or old local CSS links that match pattern?
        # Simpler: Remove ALL stylesheet links and insert our new set? 
        # CAUTIOUS: Might remove page-specific CSS. 
        # Strategy: Remove Squarespace remote CSS. Insert our local CSS at the end of <head>.
        
        # Remove remote squarespace css
        links_to_remove = []
        for link in target_soup.find_all('link', rel='stylesheet'):
            try:
                href = link.get('href', '')
                if 'squarespace.com' in href or 'sqspcdn.com' in href:
                    links_to_remove.append(link)
            except Exception as e:
                print(f"Skipping link due to error: {e}")

        for link in links_to_remove:
            link.decompose()
        
        # Insert new local CSS
        # We append them to the head.
        if target_soup.head:
            for css_tag in local_css_tags:
                # specific check to avoid duplicates if they already exist locally
                # But since we're overwriting essentially, let's just ensure we don't duplicate if we run twice.
                # For now, let's just append. simpler.
                # To do it cleanly with BS4:
                new_tag = BeautifulSoup(css_tag, 'html.parser').link
                target_soup.head.append(new_tag)
        
        # 2. Update Header
        old_header = target_soup.find('header', id='header')
        if old_header:
            # We need to parse the header_content string back into a tag to replace
            new_header_tag = BeautifulSoup(header_content, 'html.parser').header
            
            # 3. Update Active State
            # Reset all active states first
            for active_item in new_header_tag.find_all(class_='header-nav-item--active'):
                active_item['class'].remove('header-nav-item--active')
            for active_item_mobile in new_header_tag.find_all(class_='header-menu-nav-item--active'):
                active_item_mobile['class'].remove('header-menu-nav-item--active')
            for active_link in new_header_tag.find_all(attrs={'aria-current': 'page'}):
                del active_link['aria-current']

            # Find the nav item that links to this filename
            # Filenames: contact.html, etc.
            # We search for all links to cover both desktop and mobile
            target_links = new_header_tag.find_all('a', href=filename)
            for target_link in target_links:
                target_link['aria-current'] = 'page'
                # Walk up to find the nav item container
                parent = target_link.parent
                while parent and parent.name != 'nav' and parent.name != 'body':
                    if 'class' in parent.attrs: 
                        if 'header-nav-item' in parent['class'] or 'header-nav-folder-item' in parent['class']:
                             parent['class'].append('header-nav-item--active')
                             break
                        if 'header-menu-nav-item' in parent['class']:
                             parent['class'].append('header-menu-nav-item--active')
                             break
                    parent = parent.parent

            old_header.replace_with(new_header_tag)
        else:
            print(f"Warning: No header found in {filename} to replace.")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(target_soup))

    print("Synchronization complete.")

if __name__ == "__main__":
    sync_styles()
