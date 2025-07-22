/**
 * Kannada Audio Player
 * This module handles playback of pre-recorded Kannada audio files
 * and falls back to text-to-speech for unique responses.
 */

// Audio mapping for common phrases and all suggested questions
const kannadaAudioMap = {
    // Common greetings and responses
    "ನಮಸ್ಕಾರ": "/static/audio/kannada_sample.mp3",
    "ಧನ್ಯವಾದಗಳು": "/static/audio/kannada_sample.mp3",
    "ಸ್ವಾಗತ": "/static/audio/kannada_sample.mp3",
    
    // Common assistant responses
    "ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?": "/static/audio/kannada_sample.mp3",
    "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ": "/static/audio/kannada_sample.mp3",
    "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೊಮ್ಮೆ ಕೇಳಿ": "/static/audio/kannada_sample.mp3",
    
    // Government Schemes Questions
    "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಎಂದರೇನು?": "/static/audio/kannada_sample.mp3",
    "ಪಿಎಂ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿಗೆ ನಾನು ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು?": "/static/audio/kannada_sample.mp3",
    "MGNREGA ಎಂದರೇನು?": "/static/audio/kannada_sample.mp3",
    "ಪಿಎಂ ಆವಾಸ್ ಯೋಜನೆಯ ಬಗ್ಗೆ ತಿಳಿಸಿ": "/static/audio/kannada_sample.mp3",
    "ಉಜ್ವಲಾ ಯೋಜನೆಯು ಯಾವ ಪ್ರಯೋಜನಗಳನ್ನು ನೀಡುತ್ತದೆ?": "/static/audio/kannada_sample.mp3",
    
    // Health Services Questions
    "ಹತ್ತಿರದ ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆಯನ್ನು ನಾನು ಹೇಗೆ ಕಂಡುಕೊಳ್ಳಬಹುದು?": "/static/audio/kannada_sample.mp3",
    "ಸಾರ್ವತ್ರಿಕ ಲಸಿಕಾ ಕಾರ್ಯಕ್ರಮದ ಅಡಿಯಲ್ಲಿ ಯಾವ ಲಸಿಕೆಗಳನ್ನು ಉಚಿತವಾಗಿ ನೀಡಲಾಗುತ್ತದೆ?": "/static/audio/kannada_sample.mp3",
    
    // Education Questions
    "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಯಾವ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಲಭ್ಯವಿವೆ?": "/static/audio/kannada_sample.mp3",
    "ಶಿಕ್ಷಣ ಸಾಲಗಳಿಗೆ ನಾನು ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು?": "/static/audio/kannada_sample.mp3",
    
    // Governance Questions
    "ನಾನು ಭ್ರಷ್ಟಾಚಾರವನ್ನು ಹೇಗೆ ವರದಿ ಮಾಡಬಹುದು?": "/static/audio/kannada_sample.mp3",
    "ಮಾಹಿತಿ ಹಕ್ಕು ಕಾಯ್ದೆ ಎಂದರೇನು?": "/static/audio/kannada_sample.mp3",
    
    // Disaster Management Questions
    "ಪ್ರವಾಹದ ಸಮಯದಲ್ಲಿ ನಾನು ಏನು ಮಾಡಬೇಕು?": "/static/audio/kannada_sample.mp3",
    "ಭೂಕಂಪಕ್ಕೆ ನಾನು ಹೇಗೆ ಸಿದ್ಧತೆ ಮಾಡಿಕೊಳ್ಳಬಹುದು?": "/static/audio/kannada_sample.mp3",
    
    // Citizen Services Questions
    "ಭಾರತದ ನಾಗರಿಕನಾಗಿ ನನ್ನ ಹಕ್ಕುಗಳೇನು?": "/static/audio/kannada_sample.mp3",
    "ಹೊಸ ಆಧಾರ್ ಕಾರ್ಡ್ ಅನ್ನು ನಾನು ಹೇಗೆ ಪಡೆಯಬಹುದು?": "/static/audio/kannada_sample.mp3",
    "ನಾನು ಮತದಾನಕ್ಕೆ ಹೇಗೆ ನೋಂದಾಯಿಸಿಕೊಳ್ಳಬೇಕು?": "/static/audio/kannada_sample.mp3",
    
    // Common responses for Kannada
    "ನಿಮಗೆ ಬೇರೆ ಯಾವುದಾದರೂ ಪ್ರಶ್ನೆಗಳಿವೆಯೇ? ನಾನು ಸಹಾಯ ಮಾಡಲು ಸಂತೋಷಪಡುತ್ತೇನೆ.": "/static/audio/kannada_sample.mp3",
    "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರಿಸುವಲ್ಲಿ ನನಗೆ ತೊಂದರೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಒಂದನ್ನು ಪ್ರಯತ್ನಿಸಿ.": "/static/audio/kannada_sample.mp3",
    "ಕ್ಷಮಿಸಿ, ಸೇವೆಗೆ ಸಂಪರ್ಕಿಸುವಲ್ಲಿ ದೋಷವಿದೆ. ದಯವಿಟ್ಟು ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.": "/static/audio/kannada_sample.mp3",
    "ಧ್ವನಿ ಪ್ರತಿಕ್ರಿಯೆಗಳು ಈಗ ಸಕ್ರಿಯಗೊಂಡಿವೆ": "/static/audio/kannada_sample.mp3",
    "ಧ್ವನಿ ಸೇವೆ ಪ್ರಸ್ತುತ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.": "/static/audio/kannada_sample.mp3",
    
    // Default sample for demonstration
    "default": "/static/audio/kannada_sample.mp3"
};

// Audio player instance
let audioPlayer = null;

/**
 * Find the best matching audio for the given text
 * @param {string} text - The text to find audio for
 * @returns {string} - URL of the best matching audio
 */
function findBestMatchingAudio(text) {
    // First try exact match
    if (kannadaAudioMap[text]) {
        console.log(`Found exact match for: "${text}"`);
        return kannadaAudioMap[text];
    }
    
    // Try to find the longest matching phrase
    let bestMatch = "";
    let bestMatchLength = 0;
    
    for (const phrase of Object.keys(kannadaAudioMap)) {
        // Skip very short phrases to avoid false matches
        if (phrase.length < 10) continue;
        
        if (text.includes(phrase) && phrase.length > bestMatchLength) {
            bestMatch = phrase;
            bestMatchLength = phrase.length;
        }
    }
    
    if (bestMatch) {
        console.log(`Found partial match: "${bestMatch}" in "${text}"`);
        return kannadaAudioMap[bestMatch];
    }
    
    // If no match found, use default
    console.log(`No match found for: "${text}", using default`);
    return kannadaAudioMap["default"];
}

/**
 * Play Kannada audio for the given text
 * @param {string} text - The Kannada text to speak
 * @param {function} onComplete - Callback function when audio completes
 * @param {function} onError - Callback function if an error occurs
 */
function playKannadaAudio(text, onComplete, onError) {
    // Cancel any ongoing audio
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer = null;
    }
    
    // Find the best matching audio
    const audioUrl = findBestMatchingAudio(text);
    
    // Create and play audio
    audioPlayer = new Audio(audioUrl);
    
    // Set up event handlers
    audioPlayer.onended = function() {
        if (onComplete) onComplete();
    };
    
    audioPlayer.onerror = function(error) {
        console.error("Error playing Kannada audio:", error);
        if (onError) onError(error);
    };
    
    // Play the audio
    audioPlayer.play().catch(error => {
        console.error("Failed to play Kannada audio:", error);
        if (onError) onError(error);
    });
    
    return audioPlayer;
}

/**
 * Stop any currently playing Kannada audio
 */
function stopKannadaAudio() {
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer = null;
    }
}

/**
 * Check if the text contains enough Kannada characters to be considered Kannada text
 * @param {string} text - The text to check
 * @returns {boolean} - True if the text is primarily Kannada
 */
function isKannadaText(text) {
    // Kannada Unicode range: 0C80-0CFF
    const kannadaRegex = /[\u0C80-\u0CFF]/g;
    const kannadaMatches = text.match(kannadaRegex) || [];
    
    // If more than 30% of characters are Kannada, consider it Kannada text
    const kannadaPercentage = kannadaMatches.length / text.length;
    
    // Check if the text exactly matches any of our predefined Kannada phrases
    const isExactMatch = Object.keys(kannadaAudioMap).some(phrase => 
        text.includes(phrase) && phrase.length > 10);
    
    return kannadaPercentage > 0.3 || isExactMatch;
}

/**
 * Initialize Kannada voice recognition
 * @param {function} onResult - Callback function when a result is received
 * @param {function} onError - Callback function if an error occurs
 * @returns {object} - The recognition object
 */
function initKannadaVoiceRecognition(onResult, onError) {
    if (!('webkitSpeechRecognition' in window)) {
        if (onError) onError("Speech recognition not supported in this browser");
        return null;
    }
    
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'kn-IN'; // Set language to Kannada
    
    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        
        const transcript = finalTranscript || interimTranscript;
        if (onResult) onResult(transcript);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        if (onError) onError(event.error);
    };
    
    return recognition;
}

/**
 * Start Kannada voice recognition
 * @param {function} onResult - Callback function when a result is received
 * @param {function} onError - Callback function if an error occurs
 * @returns {object} - The recognition object
 */
function startKannadaVoiceRecognition(onResult, onError) {
    const recognition = initKannadaVoiceRecognition(onResult, onError);
    
    if (recognition) {
        recognition.start();
    }
    
    return recognition;
}