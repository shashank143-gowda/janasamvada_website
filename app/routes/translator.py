from flask import Blueprint, render_template, request, jsonify
import requests
import json
import os

# Create blueprint
translator_bp = Blueprint('translator', __name__)

# Dhwani API configuration
DHWANI_API = {
    "key": "shashanksmv511@gmail.com_dwani",
    "base_url": "https://dwani-dwani-api.hf.space"
}

# Supported languages
LANGUAGES = {
    "en": {"name": "English", "voice": "en-US"},
    "hi": {"name": "Hindi", "voice": "hi-IN"},
    "kn": {"name": "Kannada", "voice": "kn-IN"},
    "ta": {"name": "Tamil", "voice": "ta-IN"},
    "te": {"name": "Telugu", "voice": "te-IN"},
    "ml": {"name": "Malayalam", "voice": "ml-IN"},
    "mr": {"name": "Marathi", "voice": "mr-IN"},
    "bn": {"name": "Bengali", "voice": "bn-IN"},
    "gu": {"name": "Gujarati", "voice": "gu-IN"},
    "pa": {"name": "Punjabi", "voice": "pa-IN"}
}

@translator_bp.route('/translator')
def translator():
    """Render the translator page"""
    return render_template('translator.html', languages=LANGUAGES)

@translator_bp.route('/api/translate', methods=['POST'])
def translate():
    """API endpoint to translate text using Dhwani API"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'source_language' not in data or 'target_language' not in data:
            return jsonify({"success": False, "error": "Missing required parameters"}), 400
        
        text = data['text']
        source_language = data['source_language']
        target_language = data['target_language']
        
        # Call Dhwani API for translation
        response = requests.post(
            f"{DHWANI_API['base_url']}/translate",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DHWANI_API['key']}"
            },
            json={
                "text": text,
                "source_language": source_language,
                "target_language": target_language
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        return jsonify({
            "success": True,
            "translated_text": result.get("translated_text", ""),
            "source_language": source_language,
            "target_language": target_language
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@translator_bp.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """API endpoint for speech recognition using Dhwani API"""
    try:
        # Check if the post has the file part
        if 'audio' not in request.files:
            return jsonify({"success": False, "error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        if audio_file.filename == '':
            return jsonify({"success": False, "error": "No audio file selected"}), 400
        
        # Save the file temporarily
        temp_path = os.path.join(os.path.dirname(__file__), 'temp_audio.wav')
        audio_file.save(temp_path)
        
        # Call Dhwani API for speech recognition
        with open(temp_path, 'rb') as f:
            files = {'audio': f}
            response = requests.post(
                f"{DHWANI_API['base_url']}/speech-to-text",
                headers={
                    "Authorization": f"Bearer {DHWANI_API['key']}"
                },
                files=files,
                data={"language": language}
            )
        
        # Remove temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        response.raise_for_status()
        result = response.json()
        
        return jsonify({
            "success": True,
            "text": result.get("text", ""),
            "language": language
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@translator_bp.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """API endpoint for text-to-speech using Dhwani API"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'language' not in data:
            return jsonify({"success": False, "error": "Missing required parameters"}), 400
        
        text = data['text']
        language = data['language']
        
        # Call Dhwani API for text-to-speech
        response = requests.post(
            f"{DHWANI_API['base_url']}/text-to-speech",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DHWANI_API['key']}"
            },
            json={
                "text": text,
                "language": language
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        return jsonify({
            "success": True,
            "audio_url": result.get("audio_url", ""),
            "language": language
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@translator_bp.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for chatbot using Dhwani API"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data or 'language' not in data:
            return jsonify({"success": False, "error": "Missing required parameters"}), 400
        
        message = data['message']
        language = data['language']
        context = data.get('context', [])
        
        # Call Dhwani API for chatbot
        response = requests.post(
            f"{DHWANI_API['base_url']}/chatbot",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DHWANI_API['key']}"
            },
            json={
                "message": message,
                "language": language,
                "context": context
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Get the response text
        response_text = result.get("response", "")
        
        # Store the conversation in the database if user is logged in
        from flask_login import current_user
        if current_user.is_authenticated:
            try:
                from app.models.models import ChatbotQuery, db
                
                # Create a new chatbot query record
                query = ChatbotQuery(
                    user_id=current_user.id,
                    query=message,
                    response=response_text,
                    language=language
                )
                
                # Add and commit to database
                db.session.add(query)
                db.session.commit()
            except Exception as db_error:
                # Log the error but don't fail the request
                print(f"Error saving chatbot query: {str(db_error)}")
        
        return jsonify({
            "success": True,
            "response": response_text,
            "language": language
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@translator_bp.route('/api/voice-chatbot', methods=['POST'])
def voice_chatbot():
    """API endpoint for voice-based chatbot using Dhvani API"""
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
        temp_path = os.path.join(os.path.dirname(__file__), 'temp_audio.wav')
        audio_file.save(temp_path)
        
        # Import the Dhvani client
        from app.utils.dhvani_ai import DhvaniAI
        
        # Create a Dhvani client
        dhvani_client = DhvaniAI(
            api_key='shashanksmv511@gmail.com_dwani',
            base_url='https://dwani-dwani-api.hf.space'
        )
        
        # Step 1: Call Dhvani API for speech recognition
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
        
        # Remove temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        speech_response.raise_for_status()
        speech_result = speech_response.json()
        
        # Get the transcribed text
        message = speech_result.get("text", "")
        
        if not message:
            return jsonify({"success": False, "error": "Could not transcribe audio"}), 400
        
        # Step 2: Call Dhwani API for chatbot with the transcribed text
        chatbot_response = requests.post(
            f"{DHWANI_API['base_url']}/chatbot",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DHWANI_API['key']}"
            },
            json={
                "message": message,
                "language": language,
                "context": context
            }
        )
        
        chatbot_response.raise_for_status()
        chatbot_result = chatbot_response.json()
        
        # Get the response text
        response_text = chatbot_result.get("response", "")
        
        # Store the conversation in the database if user is logged in
        from flask_login import current_user
        if current_user.is_authenticated:
            try:
                from app.models.models import ChatbotQuery, db
                
                # Create a new chatbot query record
                query = ChatbotQuery(
                    user_id=current_user.id,
                    query=message,
                    response=response_text,
                    language=language,
                    voice_input=True
                )
                
                # Add and commit to database
                db.session.add(query)
                db.session.commit()
            except Exception as db_error:
                # Log the error but don't fail the request
                print(f"Error saving chatbot query: {str(db_error)}")
        
        return jsonify({
            "success": True,
            "transcribed_text": message,
            "response": response_text,
            "language": language
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500