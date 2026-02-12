document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Fix
    const folders = document.querySelectorAll('.header-menu-nav-folder');
    const folderToggles = document.querySelectorAll('[data-folder-id]');
    const backButtons = document.querySelectorAll('[data-action="back"]');
    const menuNav = document.querySelector('.header-menu-nav');

    // Function to open a folder
    function openFolder(folderId) {
        const targetFolder = document.querySelector(`.header-menu-nav-folder[data-folder="${folderId}"]`);
        if (targetFolder) {
            targetFolder.classList.add('header-menu-nav-folder--active');
            // Ensure the root folder stays or handles overlap correctly
            // In some SS templates, the root needs to move or be covered.
            // We'll rely on z-index and absolute positioning usually found in these templates.

            // Force visibility if needed
            targetFolder.style.transform = 'translateX(0)';
            targetFolder.style.visibility = 'visible';
            targetFolder.style.opacity = '1';
        }
    }

    // Function to close a folder (go back)
    function closeFolder(folder) {
        folder.classList.remove('header-menu-nav-folder--active');
        folder.style.transform = ''; // Revert to CSS default (likely translateX(100%))
        folder.style.visibility = '';
        folder.style.opacity = '';
    }

    // Attach click events to folder toggles
    folderToggles.forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            const folderId = this.getAttribute('data-folder-id');
            if (folderId && folderId !== '#') {
                e.preventDefault();
                openFolder(folderId);
            }
        });
    });

    // Attach click events to back buttons
    backButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const parentFolder = this.closest('.header-menu-nav-folder');
            if (parentFolder) {
                closeFolder(parentFolder);
            }
        });
    });

    // Fix for the initial broken "About Us" link in index.html if not updated in HTML yet
    // (We will update HTML, but this is a failsafe or for other pages)
    const aboutToggle = document.querySelector('a[data-folder-id="#"]');
    if (aboutToggle) {
        const folderContent = aboutToggle.querySelector('.header-menu-nav-item-content-folder');
        if (folderContent && folderContent.innerText.includes('About')) {
            aboutToggle.setAttribute('data-folder-id', '/about');
        }
    }
});
