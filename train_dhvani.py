"""
Dhvani.ai API Training Script

This script demonstrates how to use the Dhvani.ai API for:
1. Chatbot functionality
2. Speech-to-text recognition
3. Text-to-speech conversion

API Key: shashanksmv511@gmail_dwani.com
Base URL: https://dwani-dwani-api.hf.space
"""

import requests
import json
import base64
import os
import logging
from pprint import pprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API configuration
API_KEY = "shashanksmv511@gmail_dwani.com"
BASE_URL = "https://dwani-dwani-api.hf.space"

# Endpoints
CHAT_ENDPOINT = f"{BASE_URL}/chat/run"
ASR_ENDPOINT = f"{BASE_URL}/asr/run"
TTS_ENDPOINT = f"{BASE_URL}/tts/run"

def run_chat(prompt, src_lang="english", tgt_lang="kannada"):
    """
    Send a message to the Dhvani.ai chatbot
    
    Args:
        prompt (str): The user's message
        src_lang (str): Source language (default: english)
        tgt_lang (str): Target language (default: kannada)
        
    Returns:
        dict: Response from the API
    """
    try:
        # For Hugging Face Space API
        payload = {
            "data": [
                prompt,
                src_lang,
                tgt_lang
            ]
        }
        
        logger.info(f"Sending chat request with prompt: '{prompt}'")
        
        response = requests.post(
            CHAT_ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        response.raise_for_status()  # Raise exception for HTTP errors
        result = response.json()
        
        logger.info(f"Chat response received")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in chat request: {e}")
        return {"error": str(e)}

def run_asr(audio_file_path, language="kannada"):
    """
    Transcribe speech to text using Dhvani.ai ASR
    
    Args:
        audio_file_path (str): Path to the audio file
        language (str): Language of the audio (default: kannada)
        
    Returns:
        dict: Transcription result
    """
    try:
        # Read the audio file and encode as base64
        with open(audio_file_path, 'rb') as f:
            audio_bytes = f.read()
            
        # Encode as base64
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Create a data payload for the API
        payload = {
            "data": [
                audio_b64,
                language
            ]
        }
        
        logger.info(f"Sending ASR request for file: {audio_file_path}")
        
        response = requests.post(
            ASR_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"ASR response received")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in ASR request: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in ASR: {e}")
        return {"error": str(e)}

def run_tts(text, language="kannada", voice="female"):
    """
    Convert text to speech using Dhvani.ai TTS
    
    Args:
        text (str): Text to convert to speech
        language (str): Language of the text (default: kannada)
        voice (str): Voice type (default: female)
        
    Returns:
        dict: Response from the API
    """
    try:
        # For Hugging Face Space API
        payload = {
            "data": [
                text,
                language,
                voice
            ]
        }
        
        logger.info(f"Sending TTS request for text: '{text[:50]}...'")
        
        response = requests.post(
            TTS_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"TTS response received")
        
        # If the response contains a base64 encoded audio file, save it
        if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
            audio_data = result["data"][0]
            
            # Check if it's a base64 string
            if isinstance(audio_data, str) and audio_data.startswith("data:audio"):
                # Extract the base64 part
                base64_data = audio_data.split(",")[1]
                # Decode base64 to binary
                audio_binary = base64.b64decode(base64_data)
                
                # Save to file
                output_file = f"tts_output_{language}_{voice}.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_binary)
                    
                logger.info(f"TTS output saved to {output_file}")
                
                # Add file path to result
                result["file_path"] = output_file
                
            elif isinstance(audio_data, str) and audio_data.startswith("http"):
                # It's a URL to the audio file
                audio_response = requests.get(audio_data)
                audio_response.raise_for_status()
                
                # Save to file
                output_file = f"tts_output_{language}_{voice}.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_response.content)
                    
                logger.info(f"TTS output saved to {output_file}")
                
                # Add file path to result
                result["file_path"] = output_file
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in TTS request: {e}")
        return {"error": str(e)}

def main():
    """Main function to demonstrate the API usage"""
    print("=" * 50)
    print("Dhvani.ai API Training Script")
    print("=" * 50)
    
    # Test chat functionality
    print("\n1. Testing Chat Functionality")
    print("-" * 30)
    
    chat_prompts = [
        ("Hello, how are you?", "english", "kannada"),
        ("ನಮಸ್ಕಾರ, ನಿಮ್ಮ ಹೆಸರೇನು?", "kannada", "english"),
        ("What is the weather like today?", "english", "hindi")
    ]
    
    for prompt, src_lang, tgt_lang in chat_prompts:
        print(f"\nPrompt: '{prompt}' ({src_lang} -> {tgt_lang})")
        result = run_chat(prompt, src_lang, tgt_lang)
        
        if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
            print(f"Response: {result['data'][0]}")
        else:
            print("Response: No valid response received")
            print("Raw response:")
            pprint(result)
    
    # Test TTS functionality
    print("\n2. Testing Text-to-Speech Functionality")
    print("-" * 30)
    
    tts_texts = [
        ("Hello, this is a test of the text-to-speech functionality.", "english", "female"),
        ("ನಮಸ್ಕಾರ, ಇದು ಪಠ್ಯದಿಂದ ಮಾತಿಗೆ ಪರಿವರ್ತಿಸುವ ಕಾರ್ಯಕ್ಷಮತೆಯ ಪರೀಕ್ಷೆಯಾಗಿದೆ.", "kannada", "female"),
        ("नमस्ते, यह टेक्स्ट-टू-स्पीच फंक्शनैलिटी का एक परीक्षण है।", "hindi", "male")
    ]
    
    for text, language, voice in tts_texts:
        print(f"\nText: '{text[:50]}...' ({language}, {voice})")
        result = run_tts(text, language, voice)
        
        if "file_path" in result:
            print(f"Audio saved to: {result['file_path']}")
        else:
            print("Failed to generate audio")
            print("Raw response:")
            pprint(result)
    
    print("\nTraining script completed!")

if __name__ == "__main__":
    main()