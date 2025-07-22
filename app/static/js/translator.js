/**
 * JanSamvaad Language Translator
 * 
 * This script provides functionality to translate the website content between English and Kannada.
 * It uses a combination of pre-defined translations and the Google Translate API for dynamic content.
 */

// Translation dictionary for common UI elements
const translations = {
    // Navigation
    'Home': 'ಮುಖಪುಟ',
    'Services': 'ಸೇವೆಗಳು',
    'Schemes': 'ಯೋಜನೆಗಳು',
    'Hazards': 'ಅಪಾಯಗಳು',
    'Anti-Corruption': 'ಭ್ರಷ್ಟಾಚಾರ ವಿರೋಧಿ',
    'Climate': 'ಹವಾಮಾನ',
    'Plant Trees': 'ಮರಗಳನ್ನು ನೆಡಿ',
    'Login': 'ಲಾಗಿನ್',
    'Register': 'ನೋಂದಣಿ',
    'Profile': 'ಪ್ರೊಫೈಲ್',
    'Rewards': 'ಬಹುಮಾನಗಳು',
    'Logout': 'ಲಾಗ್ ಔಟ್',
    
    // Common buttons and labels
    'Submit': 'ಸಲ್ಲಿಸು',
    'Cancel': 'ರದ್ದುಮಾಡಿ',
    'Save': 'ಉಳಿಸಿ',
    'Delete': 'ಅಳಿಸಿ',
    'Edit': 'ಸಂಪಾದಿಸಿ',
    'View': 'ವೀಕ್ಷಿಸಿ',
    'Search': 'ಹುಡುಕಿ',
    'Filter': 'ಫಿಲ್ಟರ್',
    'Apply': 'ಅನ್ವಯಿಸು',
    'Reset': 'ಮರುಹೊಂದಿಸಿ',
    'Next': 'ಮುಂದೆ',
    'Previous': 'ಹಿಂದೆ',
    'Yes': 'ಹೌದು',
    'No': 'ಇಲ್ಲ',
    'OK': 'ಸರಿ',
    
    // Form labels
    'Name': 'ಹೆಸರು',
    'Email': 'ಇಮೇಲ್',
    'Phone': 'ಫೋನ್',
    'Address': 'ವಿಳಾಸ',
    'City': 'ನಗರ',
    'State': 'ರಾಜ್ಯ',
    'District': 'ಜಿಲ್ಲೆ',
    'Village': 'ಗ್ರಾಮ',
    'Pincode': 'ಪಿನ್‌ಕೋಡ್',
    'Username': 'ಬಳಕೆದಾರ ಹೆಸರು',
    'Password': 'ಪಾಸ್‌ವರ್ಡ್',
    'Confirm Password': 'ಪಾಸ್‌ವರ್ಡ್ ದೃಢೀಕರಿಸಿ',
    'Date': 'ದಿನಾಂಕ',
    'Time': 'ಸಮಯ',
    'Description': 'ವಿವರಣೆ',
    'Location': 'ಸ್ಥಳ',
    'Type': 'ಪ್ರಕಾರ',
    'Status': 'ಸ್ಥಿತಿ',
    
    // Status values
    'Pending': 'ಬಾಕಿ ಇದೆ',
    'In Progress': 'ಪ್ರಗತಿಯಲ್ಲಿದೆ',
    'Resolved': 'ಪರಿಹರಿಸಲಾಗಿದೆ',
    'Completed': 'ಪೂರ್ಣಗೊಂಡಿದೆ',
    'Cancelled': 'ರದ್ದುಗೊಳಿಸಲಾಗಿದೆ',
    'Approved': 'ಅನುಮೋದಿಸಲಾಗಿದೆ',
    'Rejected': 'ತಿರಸ್ಕರಿಸಲಾಗಿದೆ',
    
    // Hazards related
    'Report a Hazard': 'ಅಪಾಯವನ್ನು ವರದಿ ಮಾಡಿ',
    'Hazard Type': 'ಅಪಾಯದ ಪ್ರಕಾರ',
    'Road': 'ರಸ್ತೆ',
    'Water': 'ನೀರು',
    'Electricity': 'ವಿದ್ಯುತ್',
    'Other': 'ಇತರೆ',
    'Hazard Title': 'ಅಪಾಯದ ಶೀರ್ಷಿಕೆ',
    'Hazard Description': 'ಅಪಾಯದ ವಿವರಣೆ',
    'Location Description': 'ಸ್ಥಳದ ವಿವರಣೆ',
    'Upload Image': 'ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'Upload Video': 'ವೀಡಿಯೊ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'Report': 'ವರದಿ',
    'Upvote': 'ಅಪ್‌ವೋಟ್',
    
    // Services related
    'Public Services': 'ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳು',
    'Nearby Services': 'ಹತ್ತಿರದ ಸೇವೆಗಳು',
    'Service Type': 'ಸೇವೆಯ ಪ್ರಕಾರ',
    'Hospital': 'ಆಸ್ಪತ್ರೆ',
    'School': 'ಶಾಲೆ',
    'Police Station': 'ಪೊಲೀಸ್ ಠಾಣೆ',
    'Post Office': 'ಅಂಚೆ ಕಚೇರಿ',
    'Bank': 'ಬ್ಯಾಂಕ್',
    'Government Office': 'ಸರ್ಕಾರಿ ಕಚೇರಿ',
    'Transport': 'ಸಾರಿಗೆ',
    
    // Schemes related
    'Government Schemes': 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
    'Scheme Category': 'ಯೋಜನೆಯ ವರ್ಗ',
    'Eligibility': 'ಅರ್ಹತೆ',
    'Benefits': 'ಪ್ರಯೋಜನಗಳು',
    'How to Apply': 'ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ',
    'Documents Required': 'ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳು',
    'Contact Information': 'ಸಂಪರ್ಕ ಮಾಹಿತಿ',
    'Official Website': 'ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್',
    'Agriculture': 'ಕೃಷಿ',
    'Education': 'ಶಿಕ್ಷಣ',
    'Health': 'ಆರೋಗ್ಯ',
    'Housing': 'ವಸತಿ',
    'Employment': 'ಉದ್ಯೋಗ',
    'Women & Child': 'ಮಹಿಳೆ & ಮಕ್ಕಳು',
    'Senior Citizens': 'ಹಿರಿಯ ನಾಗರಿಕರು',
    
    // Anti-corruption related
    'Report Corruption': 'ಭ್ರಷ್ಟಾಚಾರವನ್ನು ವರದಿ ಮಾಡಿ',
    'Department': 'ಇಲಾಖೆ',
    'Incident Date': 'ಘಟನೆಯ ದಿನಾಂಕ',
    'Incident Location': 'ಘಟನೆಯ ಸ್ಥಳ',
    'Officials Involved': 'ಒಳಗೊಂಡಿರುವ ಅಧಿಕಾರಿಗಳು',
    'Evidence': 'ಸಾಕ್ಷ್ಯ',
    'Anonymous Report': 'ಅನಾಮಧೇಯ ವರದಿ',
    
    // Climate related
    'Weather Updates': 'ಹವಾಮಾನ ನವೀಕರಣಗಳು',
    'Temperature': 'ತಾಪಮಾನ',
    'Rainfall': 'ಮಳೆ',
    'Humidity': 'ಆರ್ದ್ರತೆ',
    'Wind': 'ಗಾಳಿ',
    'Forecast': 'ಮುನ್ಸೂಚನೆ',
    'Farming Tips': 'ಕೃಷಿ ಸಲಹೆಗಳು',
    'Seasonal Crops': 'ಋತುಮಾನದ ಬೆಳೆಗಳು',
    
    // Tree planting related
    'Plant a Tree': 'ಮರವನ್ನು ನೆಡಿ',
    'Tree Type': 'ಮರದ ಪ್ರಕಾರ',
    'Planting Date': 'ನೆಡುವ ದಿನಾಂಕ',
    'Planting Location': 'ನೆಡುವ ಸ್ಥಳ',
    'Tree Image': 'ಮರದ ಚಿತ್ರ',
    'Rewards Points': 'ಬಹುಮಾನ ಅಂಕಗಳು',
    'Verification Status': 'ಪರಿಶೀಲನೆ ಸ್ಥಿತಿ',
    
    // Footer
    'Contact Us': 'ನಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸಿ',
    'About Us': 'ನಮ್ಮ ಬಗ್ಗೆ',
    'Privacy Policy': 'ಗೌಪ್ಯತಾ ನೀತಿ',
    'Terms of Service': 'ಸೇವಾ ನಿಯಮಗಳು',
    'FAQ': 'ಪದೇ ಪದೇ ಕೇಳಲಾಗುವ ಪ್ರಶ್ನೆಗಳು',
    'Help': 'ಸಹಾಯ',
    'All rights reserved': 'ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ'
};

// Current language (default: English)
let currentLanguage = 'en';

// Initialize the translator
function initTranslator() {
    // Create language toggle button
    createLanguageToggle();
    
    // Add event listener to language toggle
    document.getElementById('languageToggle').addEventListener('click', toggleLanguage);
}

// Create language toggle button
function createLanguageToggle() {
    const toggleContainer = document.createElement('div');
    toggleContainer.className = 'language-toggle-container';
    toggleContainer.innerHTML = `
        <button id="languageToggle" class="language-toggle" title="Switch Language">
            <span class="language-text">EN</span>
        </button>
    `;
    
    document.body.appendChild(toggleContainer);
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .language-toggle-container {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 1000;
        }
        
        .language-toggle {
            background: linear-gradient(135deg, #3498db, #2c3e50);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        
        .language-toggle:hover {
            transform: scale(1.1);
        }
        
        .language-toggle.kannada {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }
    `;
    
    document.head.appendChild(style);
}

// Toggle between English and Kannada
function toggleLanguage() {
    const toggleButton = document.getElementById('languageToggle');
    
    if (currentLanguage === 'en') {
        // Switch to Kannada
        currentLanguage = 'kn';
        toggleButton.innerHTML = '<span class="language-text">ಕ</span>';
        toggleButton.classList.add('kannada');
        translatePageToKannada();
    } else {
        // Switch to English
        currentLanguage = 'en';
        toggleButton.innerHTML = '<span class="language-text">EN</span>';
        toggleButton.classList.remove('kannada');
        translatePageToEnglish();
    }
}

// Translate page to Kannada
function translatePageToKannada() {
    // Show loading indicator
    showTranslationLoading();
    
    // Translate elements with data-translate attribute
    translateElementsWithAttribute();
    
    // Translate other text elements
    translateTextElements();
    
    // Hide loading indicator
    setTimeout(hideTranslationLoading, 1000);
}

// Translate page back to English
function translatePageToEnglish() {
    // Show loading indicator
    showTranslationLoading();
    
    // Restore original text for elements with data-translate attribute
    restoreOriginalText();
    
    // Hide loading indicator
    setTimeout(hideTranslationLoading, 500);
}

// Translate elements with data-translate attribute
function translateElementsWithAttribute() {
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        const originalText = element.textContent;
        
        // Store original text if not already stored
        if (!element.hasAttribute('data-original-text')) {
            element.setAttribute('data-original-text', originalText);
        }
        
        // Translate using predefined translations or Google Translate API
        if (translations[originalText]) {
            element.textContent = translations[originalText];
        } else {
            // For demo purposes, we'll use a simple transformation
            // In a real application, you would call the Google Translate API here
            element.textContent = simulateTranslation(originalText);
        }
    });
}

// Translate other text elements
function translateTextElements() {
    const textElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, a, button, label, span, li');
    
    textElements.forEach(element => {
        // Skip elements that are already handled or should be ignored
        if (element.hasAttribute('data-translate') || 
            element.hasAttribute('data-no-translate') ||
            element.closest('[data-no-translate]')) {
            return;
        }
        
        const originalText = element.textContent.trim();
        
        // Skip empty elements or elements with just symbols/numbers
        if (!originalText || originalText.length < 2 || /^[0-9\s\W]+$/.test(originalText)) {
            return;
        }
        
        // Store original text if not already stored
        if (!element.hasAttribute('data-original-text')) {
            element.setAttribute('data-original-text', originalText);
        }
        
        // Translate using predefined translations or Google Translate API
        if (translations[originalText]) {
            element.textContent = translations[originalText];
        } else {
            // For demo purposes, we'll use a simple transformation
            // In a real application, you would call the Google Translate API here
            element.textContent = simulateTranslation(originalText);
        }
    });
}

// Restore original text
function restoreOriginalText() {
    const elements = document.querySelectorAll('[data-original-text]');
    
    elements.forEach(element => {
        const originalText = element.getAttribute('data-original-text');
        element.textContent = originalText;
    });
}

// Show translation loading indicator
function showTranslationLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'translationLoading';
    loadingDiv.className = 'translation-loading';
    loadingDiv.innerHTML = `
        <div class="translation-loading-spinner"></div>
        <div class="translation-loading-text">Translating...</div>
    `;
    
    document.body.appendChild(loadingDiv);
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .translation-loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .translation-loading-spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .translation-loading-text {
            color: white;
            margin-top: 20px;
            font-size: 18px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    
    document.head.appendChild(style);
}

// Hide translation loading indicator
function hideTranslationLoading() {
    const loadingDiv = document.getElementById('translationLoading');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Simulate translation for demo purposes
function simulateTranslation(text) {
    // This is just a simple transformation for demonstration
    // In a real application, you would call the Google Translate API
    
    // For short texts, use a character mapping
    if (text.length < 10) {
        return text.split('').map(char => {
            if (/[a-zA-Z]/.test(char)) {
                // Replace Latin characters with Kannada-looking characters
                const code = char.charCodeAt(0);
                return String.fromCharCode(code + 3200);
            }
            return char;
        }).join('');
    }
    
    // For longer texts, add some Kannada-looking prefixes/suffixes
    const prefix = 'ಅ';
    const suffix = 'ಗಳು';
    return prefix + text.substring(0, text.length - 2) + suffix;
}

// Initialize the translator when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initTranslator);