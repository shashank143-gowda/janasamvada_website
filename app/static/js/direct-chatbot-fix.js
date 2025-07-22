/**
 * Direct Chatbot Fix
 * This script provides a direct solution to the chatbot toggle issue
 */

// Execute immediately
(function() {
    console.log('Direct chatbot fix loaded');
    
    // Create a completely new toggle button
    function createNewToggleButton() {
        console.log('Creating new toggle button');
        
        // Remove any existing fallback buttons
        var existingButtons = document.querySelectorAll('.chatbot-fallback-button');
        existingButtons.forEach(function(button) {
            button.parentNode.removeChild(button);
        });
        
        // Create a new button container
        var buttonContainer = document.createElement('div');
        buttonContainer.className = 'chatbot-fallback-button';
        buttonContainer.style.position = 'fixed';
        buttonContainer.style.bottom = '30px';
        buttonContainer.style.right = '30px';
        buttonContainer.style.zIndex = '9999';
        
        // Create the button
        var button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-robot"></i>';
        button.style.width = '70px';
        button.style.height = '70px';
        button.style.borderRadius = '50%';
        button.style.background = 'linear-gradient(135deg, #3498db, #2c3e50)';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        button.style.fontSize = '24px';
        button.style.cursor = 'pointer';
        button.style.transition = 'all 0.3s ease';
        
        // Add hover effect
        button.onmouseover = function() {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.3)';
        };
        
        button.onmouseout = function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        };
        
        // Add click handler
        button.onclick = function() {
            console.log('New toggle button clicked');
            toggleChatbot();
        };
        
        // Add the button to the container
        buttonContainer.appendChild(button);
        
        // Add the container to the body
        document.body.appendChild(buttonContainer);
        
        console.log('New toggle button created');
    }
    
    // Function to toggle the chatbot
    function toggleChatbot() {
        console.log('Toggle function called');
        
        var chatbotWidget = document.getElementById('chatbotWidget');
        if (!chatbotWidget) {
            console.error('Chatbot widget not found');
            return;
        }
        
        // Get the current display state
        var currentDisplay = window.getComputedStyle(chatbotWidget).display;
        console.log('Current display:', currentDisplay);
        
        // Toggle the display
        if (currentDisplay === 'none' || currentDisplay === '') {
            chatbotWidget.style.display = 'flex';
            console.log('Chatbot shown');
        } else {
            chatbotWidget.style.display = 'none';
            console.log('Chatbot hidden');
        }
    }
    
    // Make the toggle function globally available
    window.toggleChatbot = toggleChatbot;
    
    // Set up when the DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createNewToggleButton);
    } else {
        // DOM already loaded, set up immediately
        createNewToggleButton();
    }
    
    // Also set up when the window is fully loaded
    window.addEventListener('load', createNewToggleButton);
    
    // Set up again after a short delay to ensure everything is loaded
    setTimeout(createNewToggleButton, 1000);
})();