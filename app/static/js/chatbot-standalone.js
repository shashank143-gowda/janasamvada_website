/**
 * Standalone Chatbot Script
 * This script provides a simple, reliable way to toggle the chatbot and handle chat functionality
 * using the Dhvani.ai API
 */

// Execute immediately when loaded
(function() {
    // Chatbot state
    var state = {
        messages: [],
        currentLanguage: 'en',
        isTyping: false
    };
    
    // Language mapping
    var languageMap = {
        'en': 'english',
        'hi': 'hindi',
        'kn': 'kannada',
        'ta': 'tamil',
        'te': 'telugu',
        'ml': 'malayalam',
        'mr': 'marathi',
        'bn': 'bengali',
        'gu': 'gujarati',
        'pa': 'punjabi'
    };
    
    // Function to set up the chatbot
    function setupChatbot() {
        console.log('Setting up standalone chatbot');
        
        // Get the elements
        var toggleButton = document.getElementById('chatbotToggle');
        var chatbotWidget = document.getElementById('chatbotWidget');
        var closeButton = document.getElementById('closeChatbot');
        var minimizeButton = document.getElementById('minimizeChatbot');
        var sendButton = document.getElementById('sendMessage');
        var inputField = document.getElementById('chatbotInput');
        var languageSelector = document.getElementById('chatbot-language');
        var messagesContainer = document.getElementById('chatbotMessages');
        
        // Check if required elements exist
        if (!toggleButton || !chatbotWidget) {
            console.error('Required elements not found');
            return;
        }
        
        // Set up toggle button
        toggleButton.onclick = function(e) {
            console.log('Toggle button clicked');
            
            // Get the current display state
            var currentDisplay = window.getComputedStyle(chatbotWidget).display;
            console.log('Current display:', currentDisplay);
            
            // Toggle the display
            if (currentDisplay === 'none') {
                chatbotWidget.style.display = 'flex';
                console.log('Chatbot shown');
                
                // Scroll messages to bottom
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            } else {
                chatbotWidget.style.display = 'none';
                console.log('Chatbot hidden');
            }
            
            // Prevent default action
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            return false;
        };
        
        // Set up close button
        if (closeButton) {
            closeButton.onclick = function(e) {
                console.log('Close button clicked');
                chatbotWidget.style.display = 'none';
                
                // Prevent default action
                if (e) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                
                return false;
            };
        }
        
        // Set up minimize button
        if (minimizeButton) {
            minimizeButton.onclick = function(e) {
                console.log('Minimize button clicked');
                chatbotWidget.classList.toggle('minimized');
                
                // Prevent default action
                if (e) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                
                return false;
            };
        }
        
        // Set up send button
        if (sendButton && inputField) {
            sendButton.onclick = function() {
                sendMessage();
            };
            
            // Also send on Enter key
            inputField.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }
        
        // Set up language selector
        if (languageSelector) {
            languageSelector.addEventListener('change', function() {
                state.currentLanguage = languageSelector.value;
                console.log('Language changed to:', state.currentLanguage);
            });
        }
        
        // Set up suggestion buttons
        var suggestionButtons = document.querySelectorAll('.suggestion-btn');
        if (suggestionButtons) {
            suggestionButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    if (inputField) {
                        inputField.value = button.textContent;
                        sendMessage();
                    }
                });
            });
        }
        
        console.log('Standalone chatbot setup complete');
    }
    
    // Function to send a message
    function sendMessage() {
        var inputField = document.getElementById('chatbotInput');
        if (!inputField) return;
        
        var message = inputField.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        inputField.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to API
        callChatAPI(message);
    }
    
    // Function to add a user message to the chat
    function addUserMessage(message) {
        var messagesContainer = document.getElementById('chatbotMessages');
        if (!messagesContainer) return;
        
        var messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        
        var now = new Date();
        var timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Add to state
        state.messages.push({
            role: 'user',
            content: message
        });
    }
    
    // Function to add a bot message to the chat
    function addBotMessage(message) {
        var messagesContainer = document.getElementById('chatbotMessages');
        if (!messagesContainer) return;
        
        var messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        var now = new Date();
        var timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Add to state
        state.messages.push({
            role: 'assistant',
            content: message
        });
    }
    
    // Function to add a system message to the chat
    function addSystemMessage(message) {
        var messagesContainer = document.getElementById('chatbotMessages');
        if (!messagesContainer) return;
        
        var messageElement = document.createElement('div');
        messageElement.className = 'message system-message';
        
        var now = new Date();
        var timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p><i>${escapeHtml(message)}</i></p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        if (state.isTyping) return;
        
        var messagesContainer = document.getElementById('chatbotMessages');
        if (!messagesContainer) return;
        
        var indicatorElement = document.createElement('div');
        indicatorElement.className = 'message bot-message typing-indicator';
        indicatorElement.id = 'typingIndicator';
        
        indicatorElement.innerHTML = `
            <div class="message-content">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        messagesContainer.appendChild(indicatorElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        state.isTyping = true;
    }
    
    // Function to hide typing indicator
    function hideTypingIndicator() {
        var indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
        
        state.isTyping = false;
    }
    
    // Function to call the chat API
    function callChatAPI(message) {
        // Get the language code
        var langCode = state.currentLanguage;
        var langName = languageMap[langCode] || 'english';
        
        // Prepare the request
        fetch('/dhvani/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: message,
                src_lang: langName,
                tgt_lang: langName
            })
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('API request failed: ' + response.statusText);
            }
            return response.json();
        })
        .then(function(data) {
            console.log('Chat API response:', data);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            if (data.response) {
                // Add bot response to chat
                addBotMessage(data.response);
            } else if (data.error) {
                // Show error message
                addSystemMessage('Error: ' + data.error);
            } else {
                // Fallback message
                addSystemMessage("I'm sorry, I couldn't process your request at the moment. Please try again later.");
            }
        })
        .catch(function(error) {
            console.error('Chat API error:', error);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Show error message
            addSystemMessage('Error: ' + error.message);
        });
    }
    
    // Helper function to escape HTML
    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Set up when the DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupChatbot);
    } else {
        // DOM already loaded, set up immediately
        setupChatbot();
    }
    
    // Also set up after a short delay to ensure everything is loaded
    setTimeout(setupChatbot, 500);
    
    // And set up when the window is fully loaded
    window.addEventListener('load', setupChatbot);
})();