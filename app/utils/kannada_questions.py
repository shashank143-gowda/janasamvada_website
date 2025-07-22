"""
Kannada translations of predefined questions
"""

# Dictionary mapping English questions to Kannada translations
KANNADA_QUESTIONS = {
    "What is Ayushman Bharat?": "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಎಂದರೇನು?",
    "How can I apply for PM Kisan Samman Nidhi?": "ಪಿಎಂ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿಗೆ ನಾನು ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು?",
    "What is MGNREGA?": "MGNREGA ಎಂದರೇನು?",
    "Tell me about PM Awas Yojana": "ಪಿಎಂ ಆವಾಸ್ ಯೋಜನೆಯ ಬಗ್ಗೆ ತಿಳಿಸಿ",
    "What benefits does Ujjwala Yojana provide?": "ಉಜ್ವಲಾ ಯೋಜನೆಯು ಯಾವ ಪ್ರಯೋಜನಗಳನ್ನು ನೀಡುತ್ತದೆ?",
    "How can I find the nearest government hospital?": "ಹತ್ತಿರದ ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆಯನ್ನು ನಾನು ಹೇಗೆ ಕಂಡುಕೊಳ್ಳಬಹುದು?",
    "What vaccinations are provided free under the Universal Immunization Program?": "ಸಾರ್ವತ್ರಿಕ ಲಸಿಕಾ ಕಾರ್ಯಕ್ರಮದ ಅಡಿಯಲ್ಲಿ ಯಾವ ಲಸಿಕೆಗಳನ್ನು ಉಚಿತವಾಗಿ ನೀಡಲಾಗುತ್ತದೆ?",
    "What scholarships are available for students?": "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಯಾವ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಲಭ್ಯವಿವೆ?",
    "How can I apply for education loans?": "ಶಿಕ್ಷಣ ಸಾಲಗಳಿಗೆ ನಾನು ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು?",
    "How can I report corruption?": "ನಾನು ಭ್ರಷ್ಟಾಚಾರವನ್ನು ಹೇಗೆ ವರದಿ ಮಾಡಬಹುದು?",
    "What is the Right to Information Act?": "ಮಾಹಿತಿ ಹಕ್ಕು ಕಾಯ್ದೆ ಎಂದರೇನು?",
    "What should I do during a flood?": "ಪ್ರವಾಹದ ಸಮಯದಲ್ಲಿ ನಾನು ಏನು ಮಾಡಬೇಕು?",
    "How can I prepare for an earthquake?": "ಭೂಕಂಪಕ್ಕೆ ನಾನು ಹೇಗೆ ಸಿದ್ಧತೆ ಮಾಡಿಕೊಳ್ಳಬಹುದು?",
    "What are my rights as a citizen of India?": "ಭಾರತದ ನಾಗರಿಕನಾಗಿ ನನ್ನ ಹಕ್ಕುಗಳೇನು?",
    "How can I get a new Aadhaar card?": "ಹೊಸ ಆಧಾರ್ ಕಾರ್ಡ್ ಅನ್ನು ನಾನು ಹೇಗೆ ಪಡೆಯಬಹುದು?",
    "How do I register to vote?": "ನಾನು ಮತದಾನಕ್ಕೆ ಹೇಗೆ ನೋಂದಾಯಿಸಿಕೊಳ್ಳಬೇಕು?"
}

def get_kannada_question(english_question):
    """
    Get the Kannada translation of an English question
    
    Args:
        english_question (str): The English question
        
    Returns:
        str: The Kannada translation if available, otherwise the original English question
    """
    return KANNADA_QUESTIONS.get(english_question, english_question)