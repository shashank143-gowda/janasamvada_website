/**
 * Chatbot Fix Script
 * This script adds a direct event listener to the chatbot toggle button
 */

console.log('Chatbot fix script loaded');

// Function to toggle the chatbot visibility
function toggleChatbotVisibility() {
    console.log('Toggle function called');
    const chatbotWidget = document.getElementById('chatbotWidget');
    
    if (!chatbotWidget) {
        console.error('Chatbot widget not found');
        return;
    }
    
    const computedStyle = window.getComputedStyle(chatbotWidget).display;
    console.log('Current chatbot display:', computedStyle);
    
    if (computedStyle === 'none') {
        console.log('Opening chatbot');
        chatbotWidget.style.display = 'flex';
        
        // Scroll messages to bottom if they exist
        const chatbotMessages = document.getElementById('chatbotMessages');
        if (chatbotMessages) {
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
    } else {
        console.log('Closing chatbot');
        chatbotWidget.style.display = 'none';
    }
}

// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up chatbot toggle');
    
    // Find the toggle button
    const chatbotToggle = document.getElementById('chatbotToggle');
    
    if (!chatbotToggle) {
        console.error('Chatbot toggle button not found');
        return;
    }
    
    console.log('Found chatbot toggle button, adding event listener');
    
    // Add click event listener
    chatbotToggle.addEventListener('click', function(event) {
        console.log('Chatbot toggle button clicked');
        event.preventDefault();
        toggleChatbotVisibility();
    });
    
    // Also add event listeners to minimize and close buttons
    const minimizeChatbot = document.getElementById('minimizeChatbot');
    const closeChatbot = document.getElementById('closeChatbot');
    
    if (minimizeChatbot) {
        minimizeChatbot.addEventListener('click', function() {
            console.log('Minimize button clicked');
            const chatbotWidget = document.getElementById('chatbotWidget');
            if (chatbotWidget) {
                chatbotWidget.classList.toggle('minimized');
            }
        });
    }
    
    if (closeChatbot) {
        closeChatbot.addEventListener('click', function() {
            console.log('Close button clicked');
            const chatbotWidget = document.getElementById('chatbotWidget');
            if (chatbotWidget) {
                chatbotWidget.style.display = 'none';
            }
        });
    }
});