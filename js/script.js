// Select buttons
const defaultButton = document.getElementById('default-mode-toggle');
const darkButton = document.getElementById('dark-mode-toggle');
const highContrastButton = document.getElementById('high-contrast-toggle');

// Function to update theme classes for specified elements
function updateElements(theme) {
    const paragraphs = document.querySelectorAll('p'); // Select all <p> elements
    const header = document.querySelector('header'); // Select <header>
    const footer = document.querySelector('footer'); // Select <footer>
    
    // Update paragraphs
    paragraphs.forEach((p) => {
        p.classList.remove('default-mode', 'dark-mode', 'high-contrast'); // Remove all theme classes
        p.classList.add(theme); // Add the appropriate theme class
    });

    // Update header and footer only for dark and high contrast modes
    if (header) {
        header.classList.remove('dark-mode', 'high-contrast');
        if (theme !== 'default-mode') {
            header.classList.add(theme); // Only add theme if it's not default mode
        }
    }

    if (footer) {
        footer.classList.remove('dark-mode', 'high-contrast');
        if (theme !== 'default-mode') {
            footer.classList.add(theme); // Only add theme if it's not default mode
        }
    }
}

// Apply Default Theme
defaultButton.addEventListener('click', () => {
    document.body.classList.remove('dark-mode', 'high-contrast');
    document.body.classList.add('default-mode');
    updateElements('default-mode'); // Update elements to default mode
});

// Apply Dark Theme
darkButton.addEventListener('click', () => {
    document.body.classList.remove('default-mode', 'high-contrast');
    document.body.classList.add('dark-mode');
    updateElements('dark-mode'); // Update elements to dark mode
});

// Apply High Contrast Theme
highContrastButton.addEventListener('click', () => {
    document.body.classList.remove('default-mode', 'dark-mode');
    document.body.classList.add('high-contrast');
    updateElements('high-contrast'); // Update elements to high contrast mode
});
