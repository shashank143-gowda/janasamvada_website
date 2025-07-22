from flask import Blueprint, request, jsonify, render_template, current_app
import os
from werkzeug.utils import secure_filename
import uuid
import logging
import json
from app.utils.dhvani_ai import DhvaniAI
from app.utils.train_chatbot import train_chatbot, TRAINING_DATA
from app.utils.fallback_responses import get_fallback_response
from app.utils.kannada_questions import get_kannada_question

dhvani_bp = Blueprint('dhvani_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dhvani.ai client with the specific API key and base URL
# We'll initialize it in a function to avoid the current_app context issue
def get_dhvani_client():
    return DhvaniAI(
        api_key='shashanksmv511@gmail.com_dwani',
        base_url='https://dwani-dwani-api.hf.space'
    )

@dhvani_bp.route('/')
def dhvani_page():
    """Render the Dhvani.ai integration page"""
    return render_template('dhvani.html')
    
@dhvani_bp.route('/chatbot-test')
def chatbot_test():
    """Test page for chatbot toggle functionality"""
    return render_template('chatbot_test.html')
    
@dhvani_bp.route('/chatbot-demo')
def chatbot_demo():
    """Demo page for chatbot toggle functionality"""
    return render_template('chatbot_demo.html')
    
@dhvani_bp.route('/emergency-test')
def emergency_test():
    """Emergency test page with chatbot"""
    return render_template('base.html', include_chatbot=True)
    
@dhvani_bp.route('/standalone')
def standalone_chatbot():
    """Standalone chatbot page with no dependencies"""
    return render_template('standalone_chatbot.html')
    
@dhvani_bp.route('/assistant')
def dedicated_assistant():
    """Dedicated AI assistant page"""
    # Extract all questions from training data to use as suggestions
    english_questions = [item["question"] for item in TRAINING_DATA]
    
    # Create a list of question pairs (English and Kannada)
    question_pairs = []
    for q in english_questions:
        question_pairs.append({
            "english": q,
            "kannada": get_kannada_question(q)
        })
    
    return render_template('dedicated_chatbot.html', question_pairs=question_pairs)
    
@dhvani_bp.route('/test-api')
def test_api():
    """Test the Dhvani API directly"""
    try:
        # Get a client instance
        dhvani_client = get_dhvani_client()
        
        # Test with a simple prompt
        test_prompt = "Hello, can you tell me about government services?"
        
        logger.info(f"Testing API with prompt: {test_prompt}")
        response = dhvani_client.chat(test_prompt, "english", "english")
        
        # Return the raw response for debugging
        return jsonify({
            "success": True,
            "test_prompt": test_prompt,
            "raw_response": response,
            "api_key": dhvani_client.api_key,
            "base_url": dhvani_client.base_url
        })
    except Exception as e:
        logger.error(f"Error testing API: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@dhvani_bp.route('/train-chatbot', methods=['GET', 'POST'])
def train_chatbot_route():
    """Train the chatbot with predefined data"""
    if request.method == 'POST':
        try:
            result = train_chatbot()
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error in training chatbot: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        # Display training data and form
        return render_template('train_chatbot.html', training_data=TRAINING_DATA)

@dhvani_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chatbot functionality - English and Kannada only"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        language = data.get('language', 'en')
        
        # Restrict to only English and Kannada
        if language not in ['en', 'kn']:
            language = 'en'  # Default to English if not supported
        
        # Map language codes to full names
        lang_map = {
            'en': 'english',
            'kn': 'kannada'
        }
        
        # Convert language code to full name
        dhvani_lang = lang_map.get(language)
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        # Check for fallback responses first with the correct language
        fallback_response = get_fallback_response(message, language)
        if fallback_response:
            logger.info(f"Using fallback response for: '{message}' in language: {language}")
            return jsonify({'success': True, 'response': fallback_response, 'source': 'fallback'})
        
        # Get a client instance
        dhvani_client = get_dhvani_client()
        
        logger.info(f"Chat API request: message='{message}', language='{dhvani_lang}'")
        
        try:
            # Direct call to the chat function with the appropriate language
            response = dhvani_client.chat(message, 'english', dhvani_lang)
            logger.info(f"Chat API response received for language: {dhvani_lang}")
            
            if 'error' in response:
                logger.error(f"API error: {response['error']}")
                # Try with a different prompt format
                enhanced_message = f"As a government services assistant, please answer this question: {message}"
                logger.info(f"Trying with enhanced message: '{enhanced_message}'")
                
                response = dhvani_client.chat(enhanced_message, 'english', dhvani_lang)
            
            if 'response' in response:
                return jsonify({'success': True, 'response': response['response'], 'source': 'api'})
            else:
                logger.error("No response from API")
                return jsonify({'success': False, 'error': 'No response from the API'}), 500
                
        except Exception as api_error:
            logger.error(f"API request error: {api_error}")
            
            # If API fails, use a generic response
            return jsonify({
                'success': True, 
                'response': "I'm here to help with information about government schemes and services. You can ask me about Ayushman Bharat, PM Kisan, MGNREGA, or how to apply for various government services.",
                'source': 'generic'
            })
        
    except Exception as e:
        logger.error(f"Error in chat API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@dhvani_bp.route('/api/transcribe', methods=['POST'])
def transcribe_api():
    """API endpoint for speech-to-text functionality"""
    try:
        # Check if the post request has the file part
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
            
        audio_file = request.files['audio']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        language = request.form.get('language', 'kannada')
        
        logger.info(f"Transcribe API request: language='{language}', file='{audio_file.filename}'")
        
        # Get a client instance
        dhvani_client = get_dhvani_client()
        
        # Process the audio file
        result = dhvani_client.transcribe(audio_file, language)
        logger.info(f"Transcribe API response: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in transcribe API: {e}")
        return jsonify({'error': str(e)}), 500

@dhvani_bp.route('/api/tts', methods=['POST'])
def tts_api():
    """API endpoint for text-to-speech functionality"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        voice = data.get('voice', 'female')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        logger.info(f"TTS API request: text='{text[:50]}...', language='{language}', voice='{voice}'")
        
        # Get a client instance
        dhvani_client = get_dhvani_client()
            
        # Get audio data
        audio_data = dhvani_client.text_to_speech(text, language, voice)
        
        # If it's an error response (dict), return it
        if isinstance(audio_data, dict):
            logger.error(f"TTS API error: {audio_data}")
            return jsonify(audio_data), 400
            
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the audio file
        with open(file_path, 'wb') as f:
            f.write(audio_data)
            
        # Return the URL to the audio file
        audio_url = f"/static/uploads/{filename}"
        logger.info(f"TTS API success: audio saved to {audio_url}")
        
        return jsonify({
            'success': True,
            'audio_url': audio_url
        })
        
    except Exception as e:
        logger.error(f"Error in TTS API: {e}")
        return jsonify({'error': str(e)}), 500
        
@dhvani_bp.route('/api/voice-chatbot', methods=['POST'])
def voice_chatbot():
    """API endpoint for voice-based chatbot using Dhvani API"""
    # Create a temporary file path
    temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"temp_audio_{uuid.uuid4()}.wav")
    
    try:
        # Check if the post has the file part
        if 'audio' not in request.files:
            return jsonify({"success": False, "error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        context = request.form.get('context', '[]')
        
        # Parse context if provided
        try:
            context = json.loads(context)
        except:
            context = []
        
        if audio_file.filename == '':
            return jsonify({"success": False, "error": "No audio file selected"}), 400
        
        # Save the file temporarily
        audio_file.save(temp_path)
        
        # Convert language code to full name
        lang_map = {
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
        }
        
        dhvani_lang = lang_map.get(language, 'english')
        
        try:
            # Get a client instance
            dhvani_client = get_dhvani_client()
            
            # Step 1: Transcribe the audio
            with open(temp_path, 'rb') as f:
                transcription_result = dhvani_client.transcribe(f, dhvani_lang)
            
            # Remove temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Check for errors
            if 'error' in transcription_result:
                # Return a friendly message instead of an error
                return jsonify({
                    "success": True,
                    "transcribed_text": "Sorry, I couldn't understand the audio.",
                    "response": "The voice recognition service is currently unavailable. Please type your question instead."
                })
            
            # Get the transcribed text
            message = transcription_result.get("transcript", "")
            
            if not message:
                return jsonify({
                    "success": True,
                    "transcribed_text": "Sorry, I couldn't understand the audio.",
                    "response": "I couldn't transcribe your audio. Please try speaking more clearly or type your question."
                })
            
            # Step 2: Call Dhvani API for chatbot with the transcribed text
            chatbot_result = dhvani_client.chat(message, dhvani_lang, dhvani_lang)
            
            # Check for errors
            if 'error' in chatbot_result:
                # Use a fallback response
                return jsonify({
                    "success": True,
                    "transcribed_text": message,
                    "response": "I'm here to help with information about government schemes and services. You can ask me about Ayushman Bharat, PM Kisan, MGNREGA, or how to apply for various government services."
                })
            
            # Get the response text
            response_text = chatbot_result.get("response", "")
            
            if not response_text:
                # Use a fallback response
                return jsonify({
                    "success": True,
                    "transcribed_text": message,
                    "response": "I'm here to help with information about government schemes and services. You can ask me about Ayushman Bharat, PM Kisan, MGNREGA, or how to apply for various government services."
                })
            
            return jsonify({
                "success": True,
                "transcribed_text": message,
                "response": response_text
            })
        
        except Exception as api_error:
            logger.error(f"API error in voice chatbot: {str(api_error)}")
            
            # Return a friendly message instead of an error
            return jsonify({
                "success": True,
                "transcribed_text": "Voice service unavailable",
                "response": "The voice recognition service is currently unavailable. Please type your question instead."
            })
            
    except Exception as e:
        # Log the error
        logger.error(f"Voice chatbot error: {str(e)}")
        
        # Remove temporary file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        # Return a friendly message instead of an error
        return jsonify({
            "success": True,
            "transcribed_text": "Error processing audio",
            "response": "Sorry, there was an error processing your audio. Please type your question instead."
        })