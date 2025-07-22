/**
 * Direct Chatbot Fix
 * This script directly manipulates the DOM to ensure the chatbot toggle works
 */

// Immediately execute when the script loads
(function() {
    console.log('Direct chatbot fix loaded');
    
    // Function to set up the chatbot toggle
    function setupChatbotToggle() {
        console.log('Setting up direct chatbot toggle');
        
        // Get the toggle button and chatbot widget
        const toggleButton = document.getElementById('chatbotToggle');
        const chatbotWidget = document.getElementById('chatbotWidget');
        
        if (!toggleButton) {
            console.error('Toggle button not found');
            return;
        }
        
        if (!chatbotWidget) {
            console.error('Chatbot widget not found');
            return;
        }
        
        console.log('Found toggle button and chatbot widget');
        
        // Remove any existing click listeners to avoid conflicts
        const newToggleButton = toggleButton.cloneNode(true);
        toggleButton.parentNode.replaceChild(newToggleButton, toggleButton);
        
        // Add our direct click handler
        newToggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Toggle button clicked directly');
            
            // Force toggle the display
            if (chatbotWidget.style.display === 'flex') {
                console.log('Hiding chatbot');
                chatbotWidget.style.display = 'none';
            } else {
                console.log('Showing chatbot');
                chatbotWidget.style.display = 'flex';
                
                // Scroll messages to bottom
                const messagesContainer = document.getElementById('chatbotMessages');
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            }
            
            return false;
        });
        
        // Also handle close and minimize buttons
        const closeButton = document.getElementById('closeChatbot');
        if (closeButton) {
            const newCloseButton = closeButton.cloneNode(true);
            closeButton.parentNode.replaceChild(newCloseButton, closeButton);
            
            newCloseButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Close button clicked');
                chatbotWidget.style.display = 'none';
                return false;
            });
        }
        
        const minimizeButton = document.getElementById('minimizeChatbot');
        if (minimizeButton) {
            const newMinimizeButton = minimizeButton.cloneNode(true);
            minimizeButton.parentNode.replaceChild(newMinimizeButton, minimizeButton);
            
            newMinimizeButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Minimize button clicked');
                chatbotWidget.classList.toggle('minimized');
                return false;
            });
        }
        
        console.log('Direct chatbot toggle setup complete');
    }
    
    // Set up the toggle when the DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupChatbotToggle);
    } else {
        // DOM already loaded, set up immediately
        setupChatbotToggle();
    }
    
    // Also set up again after a short delay to ensure everything is loaded
    setTimeout(setupChatbotToggle, 1000);
})();