/**
 * JanSamvaad Chatbot with Voice-to-Text Functionality
 * This script handles the chatbot interface, voice recognition, and API calls
 */

// Dhwani API configuration
const DHWANI_API = {
    key: "shashanksmv511@gmail_dwani.com",
    baseUrl: "https://dwani-dwani-api.hf.space"
};

// Supported languages
const LANGUAGES = {
    en: { name: "English", voice: "en-US" },
    hi: { name: "Hindi", voice: "hi-IN" },
    kn: { name: "Kannada", voice: "kn-IN" },
    ta: { name: "Tamil", voice: "ta-IN" },
    te: { name: "Telugu", voice: "te-IN" },
    ml: { name: "Malayalam", voice: "ml-IN" },
    mr: { name: "Marathi", voice: "mr-IN" },
    bn: { name: "Bengali", voice: "bn-IN" },
    gu: { name: "Gujarati", voice: "gu-IN" },
    pa: { name: "Punjabi", voice: "pa-IN" }
};

// Initialize the chatbot
class JanSamvaadChatbot {
    constructor() {
        this.initElements();
        this.initEvents();
        this.initSpeechRecognition();
        this.isListening = false;
        this.currentLanguage = 'en';
        this.conversationContext = [];
        
        // Hide suggestions by default
        if (this.chatbotSuggestions) {
            this.chatbotSuggestions.style.display = 'none';
        }
    }

    // Initialize DOM elements
    initElements() {
        // Chatbot elements
        this.chatbotWidget = document.getElementById('chatbotWidget');
        this.chatbotMessages = document.getElementById('chatbotMessages');
        this.chatbotInput = document.getElementById('chatbotInput');
        this.sendMessageBtn = document.getElementById('sendMessage');
        this.voiceInputBtn = document.getElementById('voiceInput');
        this.chatbotToggle = document.getElementById('chatbotToggle');
        this.minimizeChatbot = document.getElementById('minimizeChatbot');
        this.closeChatbot = document.getElementById('closeChatbot');
        this.chatbotSuggestions = document.getElementById('chatbotSuggestions');
        this.toggleSuggestionsBtn = document.getElementById('toggleSuggestions');
        this.languageSelector = document.getElementById('chatbot-language');
    }

    // Initialize event listeners
    initEvents() {
        // Send message button
        this.sendMessageBtn.addEventListener('click', () => this.sendMessage());
        
        // Voice input button
        this.voiceInputBtn.addEventListener('click', () => this.toggleSpeechRecognition());
        
        // Input field enter key
        this.chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Chatbot toggle button
        this.chatbotToggle.addEventListener('click', () => this.toggleChatbot());
        
        // Minimize button
        this.minimizeChatbot.addEventListener('click', () => this.minimizeChatbot());
        
        // Close button
        this.closeChatbot.addEventListener('click', () => this.closeChatbot());
        
        // Language selector
        this.languageSelector.addEventListener('change', () => {
            this.currentLanguage = this.languageSelector.value;
            this.updateRecognitionLanguage();
        });
        
        // Toggle suggestions button
        this.toggleSuggestionsBtn.addEventListener('click', () => {
            this.chatbotSuggestions.style.display = 
                this.chatbotSuggestions.style.display === 'none' ? 'flex' : 'none';
        });
        
        // Suggestion buttons
        const suggestionBtns = document.querySelectorAll('.suggestion-btn');
        suggestionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.chatbotInput.value = btn.textContent;
                this.sendMessage();
            });
        });
    }

    // Initialize speech recognition
    initSpeechRecognition() {
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = LANGUAGES[this.currentLanguage].voice;
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.voiceInputBtn.classList.add('listening');
                this.voiceInputBtn.innerHTML = '<i class="fas fa-stop"></i>';
                this.addSystemMessage('Listening...');
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.voiceInputBtn.classList.remove('listening');
                this.voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };
            
            this.recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                if (finalTranscript) {
                    this.chatbotInput.value = finalTranscript;
                    this.sendMessage();
                } else if (interimTranscript) {
                    this.chatbotInput.value = interimTranscript;
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                this.addSystemMessage(`Error: ${event.error}`);
                this.isListening = false;
                this.voiceInputBtn.classList.remove('listening');
                this.voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };
        } catch (error) {
            console.error('Speech recognition not supported', error);
            this.voiceInputBtn.disabled = true;
            this.voiceInputBtn.title = 'Speech recognition not supported in this browser';
        }
    }

    // Update recognition language
    updateRecognitionLanguage() {
        if (this.recognition) {
            this.recognition.lang = LANGUAGES[this.currentLanguage].voice;
        }
    }

    // Toggle speech recognition
    toggleSpeechRecognition() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    // Start listening
    startListening() {
        // Check if browser supports MediaRecorder for better audio quality
        if (navigator.mediaDevices && MediaRecorder.isTypeSupported('audio/webm')) {
            this.startMediaRecording();
        } else {
            // Fallback to Web Speech API
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Failed to start speech recognition', error);
                this.addSystemMessage('Failed to start speech recognition');
            }
        }
    }

    // Stop listening
    stopListening() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
        } else {
            try {
                this.recognition.stop();
            } catch (error) {
                console.error('Failed to stop speech recognition', error);
            }
        }
    }
    
    // Start media recording for better audio quality
    async startMediaRecording() {
        try {
            this.audioChunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            
            this.mediaRecorder.addEventListener('dataavailable', event => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            });
            
            this.mediaRecorder.addEventListener('stop', () => {
                // Stop all tracks to release the microphone
                stream.getTracks().forEach(track => track.stop());
                
                // Process the recorded audio
                this.processRecordedAudio();
            });
            
            // Start recording
            this.mediaRecorder.start();
            
            // Update UI
            this.isListening = true;
            this.voiceInputBtn.classList.add('listening');
            this.voiceInputBtn.innerHTML = '<i class="fas fa-stop"></i>';
            this.addSystemMessage('Listening... (Click again to stop)');
            
            // Auto-stop after 10 seconds to prevent very long recordings
            this.recordingTimeout = setTimeout(() => {
                if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
                    this.stopListening();
                }
            }, 10000);
            
        } catch (error) {
            console.error('Failed to start media recording', error);
            this.addSystemMessage('Failed to access microphone. Please check permissions.');
            
            // Fallback to Web Speech API
            try {
                this.recognition.start();
            } catch (fallbackError) {
                console.error('Fallback speech recognition also failed', fallbackError);
            }
        }
    }
    
    // Process the recorded audio
    async processRecordedAudio() {
        if (!this.audioChunks.length) {
            this.isListening = false;
            this.voiceInputBtn.classList.remove('listening');
            this.voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            return;
        }
        
        // Create audio blob
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        
        // Create form data for API request
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        formData.append('language', this.currentLanguage);
        formData.append('context', JSON.stringify(this.conversationContext));
        
        // Update UI
        this.isListening = false;
        this.voiceInputBtn.classList.remove('listening');
        this.voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        this.addSystemMessage('Processing your voice...');
        
        try {
            // Send to our new voice-chatbot API
            const response = await fetch('/dhvani/api/voice-chatbot', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Add user message with transcribed text
                this.addUserMessage(data.transcribed_text);
                
                // Add bot response
                this.addBotMessage(data.response);
                
                // Speak the response
                this.speakText(data.response, this.currentLanguage);
                
                // Update conversation context
                this.updateConversationContext(data.transcribed_text, data.response);
            } else {
                throw new Error(data.error || 'Failed to process voice input');
            }
        } catch (error) {
            console.error('Voice processing error:', error);
            this.addSystemMessage(`Error: ${error.message}`);
        }
    }

    // Toggle chatbot visibility
    toggleChatbot() {
        console.log('Toggle chatbot clicked');
        console.log('Current display style:', this.chatbotWidget.style.display);
        console.log('Computed style:', window.getComputedStyle(this.chatbotWidget).display);
        
        // Get the computed style to check the actual display value
        const computedStyle = window.getComputedStyle(this.chatbotWidget).display;
        
        if (computedStyle === 'none') {
            console.log('Opening chatbot');
            this.chatbotWidget.style.display = 'flex';
            this.scrollToBottom();
        } else {
            console.log('Closing chatbot');
            this.chatbotWidget.style.display = 'none';
        }
    }

    // Minimize chatbot
    minimizeChatbot() {
        this.chatbotWidget.classList.toggle('minimized');
    }

    // Close chatbot
    closeChatbot() {
        this.chatbotWidget.style.display = 'none';
    }

    // Send message to chatbot
    async sendMessage() {
        const message = this.chatbotInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addUserMessage(message);
        
        // Clear input
        this.chatbotInput.value = '';
        
        // Show typing indicator
        this.addTypingIndicator();
        
        try {
            // Call our local API endpoint that connects to Dhwani
            const response = await fetch('/dhvani/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: message,
                    src_lang: this.currentLanguage === 'en' ? 'english' : 
                             this.currentLanguage === 'hi' ? 'hindi' : 
                             this.currentLanguage === 'kn' ? 'kannada' : 
                             this.currentLanguage === 'ta' ? 'tamil' : 
                             this.currentLanguage === 'te' ? 'telugu' : 
                             this.currentLanguage === 'ml' ? 'malayalam' : 
                             this.currentLanguage === 'mr' ? 'marathi' : 
                             this.currentLanguage === 'bn' ? 'bengali' : 
                             this.currentLanguage === 'gu' ? 'gujarati' : 
                             this.currentLanguage === 'pa' ? 'punjabi' : 'english',
                    tgt_lang: this.currentLanguage === 'en' ? 'english' : 
                             this.currentLanguage === 'hi' ? 'hindi' : 
                             this.currentLanguage === 'kn' ? 'kannada' : 
                             this.currentLanguage === 'ta' ? 'tamil' : 
                             this.currentLanguage === 'te' ? 'telugu' : 
                             this.currentLanguage === 'ml' ? 'malayalam' : 
                             this.currentLanguage === 'mr' ? 'marathi' : 
                             this.currentLanguage === 'bn' ? 'bengali' : 
                             this.currentLanguage === 'gu' ? 'gujarati' : 
                             this.currentLanguage === 'pa' ? 'punjabi' : 'english'
                })
            });
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            console.log('Chatbot API response:', data);
            
            if (data.response) {
                // Add bot message to chat
                this.addBotMessage(data.response);
                
                // Speak the response if in a supported language
                this.speakText(data.response, this.currentLanguage);
                
                // Update conversation context
                this.updateConversationContext(message, data.response);
            } else if (data.error) {
                // Show error message
                this.addSystemMessage(`Error: ${data.error}`);
                console.error('Chatbot API error:', data.error);
            } else {
                // Fallback message if no response or error
                this.addSystemMessage("I'm sorry, I couldn't process your request at the moment. Please try again later.");
                console.error('Invalid response from chatbot API:', data);
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.removeTypingIndicator();
            this.addSystemMessage(`Error: ${error.message}`);
        }
    }

    // Add user message to chat
    addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
            </div>
            <div class="message-time">${time}</div>
        `;
        
        this.chatbotMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    // Add bot message to chat
    addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Process message for links and formatting
        const processedMessage = this.processMessage(message);
        
        messageElement.innerHTML = `
            <div class="message-content">
                ${processedMessage}
            </div>
            <div class="message-time">${time}</div>
        `;
        
        this.chatbotMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    // Add system message to chat
    addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message system-message';
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p><i>${this.escapeHtml(message)}</i></p>
            </div>
        `;
        
        this.chatbotMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    // Add typing indicator
    addTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator';
        typingElement.id = 'typing-indicator';
        
        typingElement.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        this.chatbotMessages.appendChild(typingElement);
        this.scrollToBottom();
    }

    // Remove typing indicator
    removeTypingIndicator() {
        const typingElement = document.getElementById('typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
    }

    // Process message for links and formatting
    processMessage(message) {
        // Convert URLs to links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        let processedMessage = message.replace(urlRegex, url => `<a href="${url}" target="_blank">${url}</a>`);
        
        // Convert line breaks to <br>
        processedMessage = processedMessage.replace(/\\n/g, '<br>');
        
        // Wrap in paragraph tags if not already formatted
        if (!processedMessage.startsWith('<p>') && !processedMessage.startsWith('<ul>')) {
            processedMessage = `<p>${processedMessage}</p>`;
        }
        
        return processedMessage;
    }

    // Update conversation context
    updateConversationContext(userMessage, botResponse) {
        // Add the current exchange to the context
        this.conversationContext.push({
            role: 'user',
            content: userMessage
        });
        
        this.conversationContext.push({
            role: 'assistant',
            content: botResponse
        });
        
        // Limit context size to prevent token limits
        if (this.conversationContext.length > 10) {
            // Keep only the last 10 messages
            this.conversationContext = this.conversationContext.slice(-10);
        }
    }

    // Speak text using browser's speech synthesis
    speakText(text, languageCode) {
        if (!text) return;
        
        // Stop any ongoing speech
        window.speechSynthesis.cancel();
        
        // Remove HTML tags for speech
        const plainText = text.replace(/<[^>]*>?/gm, '');
        
        const utterance = new SpeechSynthesisUtterance(plainText);
        utterance.lang = LANGUAGES[languageCode].voice;
        
        // Find a voice that matches the language
        const voices = window.speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang.startsWith(languageCode) || v.lang.startsWith(LANGUAGES[languageCode].voice));
        
        if (voice) {
            utterance.voice = voice;
        }
        
        window.speechSynthesis.speak(utterance);
    }

    // Scroll chat to bottom
    scrollToBottom() {
        this.chatbotMessages.scrollTop = this.chatbotMessages.scrollHeight;
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize speech synthesis voices
function initVoices() {
    return new Promise((resolve) => {
        let voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            resolve(voices);
        } else {
            window.speechSynthesis.onvoiceschanged = () => {
                voices = window.speechSynthesis.getVoices();
                resolve(voices);
            };
        }
    });
}

// Initialize the chatbot when the DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        console.log('Initializing chatbot...');
        await initVoices();
        window.chatbot = new JanSamvaadChatbot();
        console.log('Chatbot initialized successfully');
        
        // Add a direct event listener to the toggle button
        const chatbotToggle = document.getElementById('chatbotToggle');
        if (chatbotToggle) {
            console.log('Found chatbot toggle button');
            chatbotToggle.addEventListener('click', function() {
                console.log('Toggle button clicked directly');
                if (window.chatbot) {
                    window.chatbot.toggleChatbot();
                } else {
                    console.error('Chatbot not initialized');
                    // Fallback toggle if chatbot isn't initialized
                    const chatbotWidget = document.getElementById('chatbotWidget');
                    if (chatbotWidget) {
                        const computedStyle = window.getComputedStyle(chatbotWidget).display;
                        chatbotWidget.style.display = computedStyle === 'none' ? 'flex' : 'none';
                    }
                }
            });
        } else {
            console.error('Chatbot toggle button not found');
        }
    } catch (error) {
        console.error('Error initializing chatbot:', error);
    }
});