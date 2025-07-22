/**
 * Enhanced Translator using Dhwani API
 * This script handles speech recognition, translation, and text-to-speech functionality
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

// Initialize the translator
class EnhancedTranslator {
    constructor() {
        this.initElements();
        this.initEvents();
        this.initSpeechRecognition();
        this.isListening = false;
        this.currentLanguage = 'en';
        this.targetLanguage = 'hi';
    }

    // Initialize DOM elements
    initElements() {
        // Input elements
        this.inputText = document.getElementById('input-text');
        this.outputText = document.getElementById('output-text');
        this.sourceLanguage = document.getElementById('source-language');
        this.targetLanguageSelect = document.getElementById('target-language');
        
        // Button elements
        this.translateBtn = document.getElementById('translate-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.speakInputBtn = document.getElementById('speak-input-btn');
        this.speakOutputBtn = document.getElementById('speak-output-btn');
        this.micBtn = document.getElementById('mic-btn');
        this.swapBtn = document.getElementById('swap-btn');
        this.copyInputBtn = document.getElementById('copy-input-btn');
        this.copyOutputBtn = document.getElementById('copy-output-btn');
        
        // Status elements
        this.translationStatus = document.getElementById('translation-status');
    }

    // Initialize event listeners
    initEvents() {
        // Translation button
        this.translateBtn.addEventListener('click', () => this.translate());
        
        // Clear button
        this.clearBtn.addEventListener('click', () => this.clearText());
        
        // Speech buttons
        this.speakInputBtn.addEventListener('click', () => this.speakText(this.inputText.value, this.sourceLanguage.value));
        this.speakOutputBtn.addEventListener('click', () => this.speakText(this.outputText.value, this.targetLanguageSelect.value));
        
        // Microphone button
        this.micBtn.addEventListener('click', () => this.toggleSpeechRecognition());
        
        // Swap languages button
        this.swapBtn.addEventListener('click', () => this.swapLanguages());
        
        // Copy buttons
        this.copyInputBtn.addEventListener('click', () => this.copyToClipboard(this.inputText.value));
        this.copyOutputBtn.addEventListener('click', () => this.copyToClipboard(this.outputText.value));
        
        // Language change events
        this.sourceLanguage.addEventListener('change', () => {
            this.currentLanguage = this.sourceLanguage.value;
            this.updateRecognitionLanguage();
        });
        
        this.targetLanguageSelect.addEventListener('change', () => {
            this.targetLanguage = this.targetLanguageSelect.value;
        });
        
        // Auto translate on input
        this.inputText.addEventListener('input', debounce(() => {
            if (this.inputText.value.trim().length > 0) {
                this.translate();
            }
        }, 1000));
    }

    // Initialize speech recognition
    initSpeechRecognition() {
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = LANGUAGES[this.currentLanguage].voice;
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.micBtn.classList.add('listening');
                this.micBtn.innerHTML = '<i class="fas fa-stop"></i>';
                this.showStatus('Listening...', 'info');
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.micBtn.classList.remove('listening');
                this.micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
                this.showStatus('Stopped listening', 'info');
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
                    this.inputText.value = finalTranscript;
                    this.translate();
                } else if (interimTranscript) {
                    this.inputText.value = interimTranscript;
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                this.showStatus(`Error: ${event.error}`, 'error');
                this.isListening = false;
                this.micBtn.classList.remove('listening');
                this.micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };
        } catch (error) {
            console.error('Speech recognition not supported', error);
            this.micBtn.disabled = true;
            this.micBtn.title = 'Speech recognition not supported in this browser';
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
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start speech recognition', error);
            this.showStatus('Failed to start speech recognition', 'error');
        }
    }

    // Stop listening
    stopListening() {
        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Failed to stop speech recognition', error);
        }
    }

    // Translate text using Dhwani API
    async translate() {
        const text = this.inputText.value.trim();
        if (!text) return;
        
        const sourceLang = this.sourceLanguage.value;
        const targetLang = this.targetLanguageSelect.value;
        
        this.showStatus('Translating...', 'info');
        
        try {
            const response = await fetch(`${DHWANI_API.baseUrl}/translate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${DHWANI_API.key}`
                },
                body: JSON.stringify({
                    text: text,
                    source_language: sourceLang,
                    target_language: targetLang
                })
            });
            
            if (!response.ok) {
                throw new Error(`Translation failed: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.translated_text) {
                this.outputText.value = data.translated_text;
                this.showStatus('Translation complete', 'success');
            } else {
                throw new Error('No translation returned');
            }
        } catch (error) {
            console.error('Translation error:', error);
            this.showStatus(`Translation error: ${error.message}`, 'error');
        }
    }

    // Speak text using browser's speech synthesis
    speakText(text, languageCode) {
        if (!text) return;
        
        // Stop any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = LANGUAGES[languageCode].voice;
        
        // Find a voice that matches the language
        const voices = window.speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang.startsWith(languageCode) || v.lang.startsWith(LANGUAGES[languageCode].voice));
        
        if (voice) {
            utterance.voice = voice;
        }
        
        window.speechSynthesis.speak(utterance);
    }

    // Clear text fields
    clearText() {
        this.inputText.value = '';
        this.outputText.value = '';
        this.showStatus('Text cleared', 'info');
    }

    // Swap languages
    swapLanguages() {
        const sourceValue = this.sourceLanguage.value;
        const targetValue = this.targetLanguageSelect.value;
        
        this.sourceLanguage.value = targetValue;
        this.targetLanguageSelect.value = sourceValue;
        
        // Swap text if there's content
        if (this.outputText.value) {
            const temp = this.inputText.value;
            this.inputText.value = this.outputText.value;
            this.outputText.value = temp;
        }
        
        // Update recognition language
        this.currentLanguage = this.sourceLanguage.value;
        this.targetLanguage = this.targetLanguageSelect.value;
        this.updateRecognitionLanguage();
        
        this.showStatus('Languages swapped', 'info');
    }

    // Copy text to clipboard
    copyToClipboard(text) {
        if (!text) return;
        
        navigator.clipboard.writeText(text)
            .then(() => {
                this.showStatus('Copied to clipboard', 'success');
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                this.showStatus('Failed to copy text', 'error');
            });
    }

    // Show status message
    showStatus(message, type = 'info') {
        this.translationStatus.textContent = message;
        this.translationStatus.className = `status status-${type}`;
        
        // Clear status after 3 seconds
        setTimeout(() => {
            this.translationStatus.textContent = '';
            this.translationStatus.className = 'status';
        }, 3000);
    }
}

// Debounce function to limit how often a function can be called
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
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

// Initialize the translator when the DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    await initVoices();
    window.translator = new EnhancedTranslator();
});