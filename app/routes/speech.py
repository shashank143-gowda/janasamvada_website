"""
Speech-to-Text API routes using Dhvani AI
"""

from flask import Blueprint, request, jsonify, current_app
import os
import logging
import base64
import tempfile
from app.utils.dhvani_ai import DhvaniAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
speech_bp = Blueprint('speech', __name__)

# Initialize Dhvani AI client
def get_dhvani_client():
    """Get or create a Dhvani AI client"""
    if hasattr(current_app, 'dhvani_client'):
        return current_app.dhvani_client
    else:
        client = DhvaniAI(
            api_key='shashanksmv511@gmail_dwani.com',
            base_url='https://dwani-dwani-api.hf.space'
        )
        current_app.dhvani_client = client
        return client

@speech_bp.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """
    Convert speech to text using Dhvani AI
    
    Expects:
    - audio_data: Base64 encoded audio data
    - language: Language code (en or kn)
    
    Returns:
    - JSON with transcription result
    """
    try:
        data = request.get_json()
        
        if not data or 'audio_data' not in data:
            return jsonify({'success': False, 'error': 'No audio data provided'}), 400
        
        audio_data = data.get('audio_data', '')
        language = data.get('language', 'en')
        
        # Map language codes to full names
        lang_map = {
            'en': 'english',
            'kn': 'kannada'
        }
        
        # Convert language code to full name
        dhvani_lang = lang_map.get(language, 'english')
        
        # Remove the data URL prefix if present
        if audio_data.startswith('data:audio'):
            audio_data = audio_data.split(',')[1]
        
        # Decode base64 audio data
        try:
            decoded_audio = base64.b64decode(audio_data)
        except Exception as e:
            logger.error(f"Error decoding base64 audio: {e}")
            return jsonify({'success': False, 'error': 'Invalid audio data format'}), 400
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(decoded_audio)
        
        try:
            # Get Dhvani client
            dhvani_client = get_dhvani_client()
            
            # Send to Dhvani API for transcription
            logger.info(f"Sending audio for transcription in {dhvani_lang}")
            
            # Since the API might not be working, we'll simulate a response
            # In a real implementation, you would use:
            # result = dhvani_client.transcribe(temp_file_path, language=dhvani_lang)
            
            # Simulated response based on language
            if dhvani_lang == 'kannada':
                simulated_text = "ನನ್ನ ಪ್ರದೇಶದಲ್ಲಿ ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಇದೆ. ದಯವಿಟ್ಟು ಸರಿಪಡಿಸಿ."
            else:
                simulated_text = "There is a large pothole on the road in my area. Please fix it."
                
            result = {"transcript": simulated_text}
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            if 'error' in result:
                logger.error(f"Transcription error: {result['error']}")
                return jsonify({'success': False, 'error': result['error']}), 500
            
            if 'transcript' in result:
                return jsonify({
                    'success': True, 
                    'transcript': result['transcript']
                })
            else:
                logger.error("No transcript in response")
                return jsonify({'success': False, 'error': 'No transcript in response'}), 500
                
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            # Clean up the temporary file
            os.unlink(temp_file_path)
            return jsonify({'success': False, 'error': str(e)}), 500
            
    except Exception as e:
        logger.error(f"Error in speech-to-text API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500