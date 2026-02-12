import os
from bs4 import BeautifulSoup

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if style already exists to avoid duplication
        style_id = "custom-navbar-style"
        existing_style = soup.find('style', id=style_id)
        
        css_content = """
        /* Custom Navbar Styling */
        .header-layout-nav-right .header-nav {
            text-align: center !important;
            flex: 1 1 auto !important; /* Allow it to take up space to center */
        }
        
        .header-nav-list {
            justify-content: center !important;
            display: flex !important;
            flex-wrap: wrap !important;
        }
        
        .header-nav-item {
            margin-left: 20px !important;
            margin-right: 20px !important;
        }
        
        /* Ensure title doesn't force nav to right if they are flex siblings */
        .header-title-nav-wrapper {
            display: flex !important;
            flex-direction: column !important; /* Stack logo and nav for true centering if needed, or adjust flex */
            align-items: center !important;
        }
        
        /* Adjusting for the specific layout where logo is separate */
        /* If we want logo on left/center and nav below or center, the above helps. 
           But if user wants Logo ... Nav(Center) ... Actions, that's different.
           User code: header-layout-nav-right. 
           Let's try to center the nav items within the nav container first. */
           
        .header-title-nav-wrapper {
             flex-direction: row !important;
             justify-content: space-between !important;
        }
        
        /* Override specifically to center the nav block itself if it was right-aligned */
        .header-nav {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important; 
        }
        
        /* Let's refine based on the structure:
           .header-inner
             .header-display-desktop
               .header-title-nav-wrapper
                 .header-title (Logo)
                 .header-nav
        */
        
        @media (min-width: 1000px) {
            .header-title-nav-wrapper {
                flex-wrap: wrap !important;
                justify-content: center !important; 
                position: relative !important;
            }
            
            .header-title {
                margin-right: auto !important; /* Keep logo left if possible, or center it too? User said "navbar option in centre" */
                /* Usually "navbar option in centre" implies the links are centered. */
            }
            
            .header-nav {
                 position: absolute !important;
                 left: 50% !important;
                 transform: translateX(-50%) !important;
                 width: auto !important;
            }
        }
        """
        
        # Simplest approach for "navbar option in center" usually means centering the nav items 
        # while keeping logo on left. Absolute positioning is risky if overlap occurs.
        # Let's try Flexbox centering.
        
        final_css = """
        <style id="custom-navbar-style">
        @media (min-width: 1000px) {
            /* Force the wrapper to allow centering */
            .header-display-desktop {
                display: flex !important;
                align-items: center !important;
            }
            
            .header-title-nav-wrapper {
                flex: 1 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important; /* Logo left, Nav center? No, this spreads them. */
            }
            
            /* To center nav items explicitly: */
            .header-nav {
                margin-left: auto !important;
                margin-right: auto !important;
            }
            
            .header-nav-list {
                display: flex !important;
                justify-content: center !important;
                gap: 2vw !important; /* Space between items */
            }

            .header-nav-item {
                margin: 0 15px !important; /* Explicit spacing */
            }
            
            /* Remove default margins if any interfering */
            .header-nav-item--folder, .header-nav-item--collection {
                
            }
        }
        </style>
        """
        
        # Parsing the CSS string to insert it as a tag
        new_style_tag = soup.new_tag("style", id=style_id)
        new_style_tag.string = """
        @media (min-width: 1000px) {
            .header-title-nav-wrapper {
                display: flex !important;
                align-items: center !important;
                width: 100% !important;
            }
            
            .header-title {
                flex: 0 0 auto !important;
            }
            
            .header-nav {
                flex: 1 1 auto !important;
                display: flex !important;
                justify-content: center !important;
            }
            
            .header-nav-list {
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
            }
            
            .header-nav-item {
                margin: 0 25px !important; /* Increased spacing */
            }
        }
        """
        
        if existing_style:
            existing_style.replace_with(new_style_tag)
            print(f"Updated style in {filepath}")
        else:
            soup.head.append(new_style_tag)
            print(f"Added style to {filepath}")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Main execution
directory = '/Users/apple/Downloads/tpcschoolrr'
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        process_file(os.path.join(directory, filename))
