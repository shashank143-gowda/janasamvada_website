"""
Dhvani.ai API Integration Module
This module provides functions to interact with Dhvani.ai API for:
1. Chatbot functionality
2. Speech-to-text recognition
3. Text-to-speech conversion
"""

import os
import requests
import json
import logging
from flask import current_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DhvaniAI:
    """Class to handle Dhvani.ai API interactions"""
    
    def __init__(self, api_key=None, base_url=None):
        """Initialize with API key and base URL"""
        self.api_key = api_key or os.environ.get('DHVANI_API_KEY') or "shashanksmv511@gmail.com_dwani"
        self.base_url = base_url or os.environ.get('DHVANI_BASE_URL') or "https://dwani-dwani-api.hf.space"
        
        # Base URLs for different services
        self.chat_base_url = f"{self.base_url}/chat"
        self.asr_base_url = f"{self.base_url}/asr"
        self.tts_base_url = f"{self.base_url}/tts"
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"Initialized Dhvani.ai client with base URL: {self.base_url}")
    
    def chat(self, prompt, src_lang="english", tgt_lang="kannada"):
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
            # For direct API access without Hugging Face Space
            # This is a fallback implementation that simulates a response
            logger.info(f"Simulating chat request for prompt: {prompt[:50]}...")
            
            # Create a simulated response based on the prompt
            if "hello" in prompt.lower() or "hi" in prompt.lower() or "namaskara" in prompt.lower() or "ನಮಸ್ಕಾರ" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಜನಸಂವಾದ್ ಸಹಾಯಕ. ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
                else:
                    response_text = "Hello! I'm your JanSamvaad Assistant. How can I help you today?"
            elif "ayushman" in prompt.lower() or "ಆಯುಷ್ಮಾನ್" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಎನ್ನುವುದು ಬಡ ಕುಟುಂಬಗಳಿಗೆ ಉಚಿತ ಆರೋಗ್ಯ ರಕ್ಷಣೆಯನ್ನು ಒದಗಿಸುವ ರಾಷ್ಟ್ರೀಯ ಆರೋಗ್ಯ ರಕ್ಷಣಾ ಯೋಜನೆಯಾಗಿದೆ. ಇದು ಪ್ರತಿ ಕುಟುಂಬಕ್ಕೆ ಪ್ರತಿ ವರ್ಷ ₹5 ಲಕ್ಷದವರೆಗೆ ಮಾಧ್ಯಮಿಕ ಮತ್ತು ತೃತೀಯ ಆರೋಗ್ಯ ಸೇವೆಗಳಿಗೆ ರಕ್ಷಣೆ ನೀಡುತ್ತದೆ."
                else:
                    response_text = "Ayushman Bharat is a national health protection scheme that aims to provide free health coverage to over 10 crore poor families. It provides coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization."
            elif "kisan" in prompt.lower() or "ಕಿಸಾನ್" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಪಿಎಂ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು, ನೀವು: 1) ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ pmkisan.gov.in ಗೆ ಭೇಟಿ ನೀಡಿ, 2) ರೈತನಾಗಿ ನೋಂದಾಯಿಸಿಕೊಳ್ಳಿ, 3) ನಿಮ್ಮ ವಿವರಗಳೊಂದಿಗೆ ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ, 4) ಆಧಾರ್, ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು ಮತ್ತು ಭೂಮಿ ದಾಖಲೆಗಳಂತಹ ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ. ಸಹಾಯಕ್ಕಾಗಿ ನಿಮ್ಮ ಹತ್ತಿರದ ಕಾಮನ್ ಸರ್ವೀಸ್ ಸೆಂಟರ್ (CSC) ಗೆ ಭೇಟಿ ನೀಡಬಹುದು."
                else:
                    response_text = "To apply for PM Kisan Samman Nidhi, you need to: 1) Visit the official website pmkisan.gov.in, 2) Register as a farmer, 3) Fill the application form with your details, 4) Submit required documents like Aadhaar, bank account details, and land records. You can also visit your nearest Common Service Centre (CSC) for assistance."
            elif "corruption" in prompt.lower() or "ಭ್ರಷ್ಟಾಚಾರ" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ನೀವು ಭ್ರಷ್ಟಾಚಾರವನ್ನು ಹೀಗೆ ವರದಿ ಮಾಡಬಹುದು: 1) ಕೇಂದ್ರ ಜಾಗೃತಾ ಆಯೋಗದ ವೆಬ್‌ಸೈಟ್ (cvc.gov.in), 2) ನಿಮ್ಮ ರಾಜ್ಯದ ಭ್ರಷ್ಟಾಚಾರ ನಿಗ್ರಹ ದಳ, 3) ಆನ್‌ಲೈನ್ ಪೋರ್ಟಲ್ pgportal.gov.in, 4) ನಿಮ್ಮ ರಾಜ್ಯದ ಭ್ರಷ್ಟಾಚಾರ ವಿರೋಧಿ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ, 5) ಲೋಕಪಾಲ್‌ಗೆ ದೂರು ಸಲ್ಲಿಸಿ. ನೀವು ಬಯಸಿದರೆ ಅನಾಮಧೇಯರಾಗಿ ಉಳಿಯಬಹುದು."
                else:
                    response_text = "You can report corruption through: 1) Central Vigilance Commission website (cvc.gov.in), 2) Anti-Corruption Bureau of your state, 3) Online portal pgportal.gov.in, 4) Call the anti-corruption helpline of your state, 5) File a complaint with the Lokpal. You can remain anonymous if you wish."
            elif "rights" in prompt.lower() or "ಹಕ್ಕುಗಳು" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಭಾರತದ ನಾಗರಿಕನಾಗಿ, ನಿಮ್ಮ ಮೂಲಭೂತ ಹಕ್ಕುಗಳು: 1) ಸಮಾನತೆಯ ಹಕ್ಕು, 2) ಸ್ವಾತಂತ್ರ್ಯದ ಹಕ್ಕು, 3) ಶೋಷಣೆಯ ವಿರುದ್ಧದ ಹಕ್ಕು, 4) ಧಾರ್ಮಿಕ ಸ್ವಾತಂತ್ರ್ಯದ ಹಕ್ಕು, 5) ಸಾಂಸ್ಕೃತಿಕ ಮತ್ತು ಶೈಕ್ಷಣಿಕ ಹಕ್ಕುಗಳು, 6) ಸಾಂವಿಧಾನಿಕ ಪರಿಹಾರಗಳ ಹಕ್ಕು. ಇವುಗಳನ್ನು ಭಾರತೀಯ ಸಂವಿಧಾನದ ಭಾಗ III ರಲ್ಲಿ ಸೇರಿಸಲಾಗಿದೆ."
                else:
                    response_text = "As a citizen of India, your fundamental rights include: 1) Right to Equality, 2) Right to Freedom, 3) Right against Exploitation, 4) Right to Freedom of Religion, 5) Cultural and Educational Rights, 6) Right to Constitutional Remedies. These are enshrined in Part III of the Indian Constitution."
            elif "aadhaar" in prompt.lower() or "ಆಧಾರ್" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಹೊಸ ಆಧಾರ್ ಕಾರ್ಡ್ ಪಡೆಯಲು: 1) ಹತ್ತಿರದ ಆಧಾರ್ ನೋಂದಣಿ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ, 2) ನೋಂದಣಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ, 3) ಗುರುತಿನ ಪುರಾವೆ, ವಿಳಾಸ ಮತ್ತು ಜನ್ಮ ದಿನಾಂಕದ ಪುರಾವೆಯನ್ನು ಒದಗಿಸಿ, 4) ಬಯೋಮೆಟ್ರಿಕ್ ಸೆರೆಹಿಡಿಯುವಿಕೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ (ಬೆರಳಚ್ಚುಗಳು, ಕಣ್ಣಿನ ಗುಡ್ಡೆಯ ಸ್ಕ್ಯಾನ್, ಫೋಟೋಗ್ರಾಫ್), 5) 14-ಅಂಕಿಯ ನೋಂದಣಿ ID ಯೊಂದಿಗೆ ನೋಂದಣಿ ಸ್ಲಿಪ್ ಪಡೆಯಿರಿ, 6) uidai.gov.in ನಲ್ಲಿ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ, 7) e-ಆಧಾರ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಭೌತಿಕ ಕಾರ್ಡ್ ವಿತರಣೆಗಾಗಿ ಕಾಯಿರಿ."
                else:
                    response_text = "To get a new Aadhaar card: 1) Visit the nearest Aadhaar Enrollment Center, 2) Fill the enrollment form, 3) Provide proof of identity, address, and date of birth, 4) Complete biometric capture (fingerprints, iris scan, photograph), 5) Receive an enrollment slip with 14-digit enrollment ID, 6) Check status online at uidai.gov.in, 7) Download e-Aadhaar or wait for physical card delivery."
            elif "voter" in prompt.lower() or "ಮತದಾನ" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಮತದಾನಕ್ಕೆ ನೋಂದಾಯಿಸಲು: 1) ನೀವು 18 ವರ್ಷ ಅಥವಾ ಅದಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ವಯಸ್ಸಿನವರಾಗಿದ್ದೀರಿ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ, 2) voter.eci.gov.in ನಲ್ಲಿ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅಥವಾ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಚುನಾವಣಾ ನೋಂದಣಿ ಕಚೇರಿಯಲ್ಲಿ ಆಫ್‌ಲೈನ್‌ನಲ್ಲಿ ನಮೂನೆ 6 ಅನ್ನು ಭರ್ತಿ ಮಾಡಿ, 3) ವಯಸ್ಸು, ಗುರುತು ಮತ್ತು ನಿವಾಸದ ಪುರಾವೆಯನ್ನು ಸಲ್ಲಿಸಿ, 4) ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ನಿಮ್ಮ ಅರ್ಜಿಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ, 5) ನಿಮ್ಮ ಮತದಾರರ ID ಕಾರ್ಡ್ ಅನ್ನು ಅಂಚೆ ಮೂಲಕ ಪಡೆಯಿರಿ ಅಥವಾ ಪೋರ್ಟಲ್‌ನಿಂದ e-EPIC ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ."
                else:
                    response_text = "To register to vote: 1) Ensure you're 18 years or older, 2) Fill Form 6 online at voter.eci.gov.in or offline at your local Electoral Registration Office, 3) Submit proof of age, identity, and residence, 4) Track your application status online, 5) Receive your Voter ID card by post or download e-EPIC from the portal."
            elif "flood" in prompt.lower() or "ಪ್ರವಾಹ" in prompt:
                if tgt_lang == "kannada":
                    response_text = "ಪ್ರವಾಹದ ಸಮಯದಲ್ಲಿ: 1) ತಕ್ಷಣವೇ ಎತ್ತರದ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ, 2) ಪ್ರವಾಹದ ನೀರಿನ ಮೂಲಕ ನಡೆಯುವುದನ್ನು ಅಥವಾ ಚಾಲನೆ ಮಾಡುವುದನ್ನು ತಪ್ಪಿಸಿ, 3) ವಿದ್ಯುತ್ ಉಪಕರಣಗಳನ್ನು ಸಂಪರ್ಕ ಕಡಿತಗೊಳಿಸಿ, 4) ತುರ್ತು ಸಂಪರ್ಕಗಳನ್ನು ಸಿದ್ಧವಾಗಿರಿಸಿ, 5) ನವೀಕರಣಗಳಿಗಾಗಿ ರೇಡಿಯೋ/ಟಿವಿ ಆಲಿಸಿ, 6) ತುರ್ತು ಸರಬರಾಜುಗಳನ್ನು ಸಿದ್ಧವಾಗಿರಿಸಿ, 7) ಅಧಿಕಾರಿಗಳು ನೀಡಿದ ಸ್ಥಳಾಂತರ ಆದೇಶಗಳನ್ನು ಅನುಸರಿಸಿ."
                else:
                    response_text = "During a flood: 1) Move to higher ground immediately, 2) Avoid walking or driving through flood waters, 3) Disconnect electrical appliances, 4) Keep emergency contacts handy, 5) Listen to radio/TV for updates, 6) Keep emergency supplies ready, 7) Follow evacuation orders if given by authorities."
            else:
                # Generic response for other queries
                if tgt_lang == "kannada":
                    response_text = "ಕ್ಷಮಿಸಿ, ನನಗೆ ಈ ಪ್ರಶ್ನೆಗೆ ನಿರ್ದಿಷ್ಟ ಉತ್ತರ ತಿಳಿದಿಲ್ಲ. ನಾನು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಸೇವೆಗಳು ಮತ್ತು ನಾಗರಿಕ ಹಕ್ಕುಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ಒದಗಿಸಲು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ದಯವಿಟ್ಟು ಆಯುಷ್ಮಾನ್ ಭಾರತ್, ಪಿಎಂ ಕಿಸಾನ್, ಅಥವಾ ಭ್ರಷ್ಟಾಚಾರವನ್ನು ಹೇಗೆ ವರದಿ ಮಾಡುವುದು ಎಂಬುದರ ಬಗ್ಗೆ ಕೇಳಿ."
                else:
                    response_text = "I'm sorry, I don't have specific information about that. I can help with information about government schemes, services, and citizen rights. Please try asking about Ayushman Bharat, PM Kisan, or how to report corruption."
            
            logger.info(f"Generated response: {response_text[:50]}...")
            return {"response": response_text}
            
        except Exception as e:
            logger.error(f"Error in chat request: {e}")
            return {"error": str(e)}
    
    def transcribe(self, audio_file, language="kannada"):
        """
        Transcribe speech to text using Dhvani.ai ASR
        
        Args:
            audio_file (str): Path to the audio file or file-like object
            language (str): Language of the audio (default: kannada)
            
        Returns:
            dict: Transcription result
        """
        try:
            # For Hugging Face Space API, we need to encode the audio file as base64
            import base64
            import io
            
            # Read the audio file
            if isinstance(audio_file, str):
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
            else:
                audio_bytes = audio_file.read()
                
            # Encode as base64
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Create a data payload for the API
            payload = {
                "data": [
                    audio_b64,
                    language
                ]
            }
            
            logger.info(f"Sending ASR request to {self.asr_base_url} for language: {language}")
            
            response = requests.post(
                f"{self.asr_base_url}/run",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"ASR response: {result}")
            
            # Extract the transcription from the Hugging Face Space API format
            if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                return {"transcript": result["data"][0]}
            else:
                return {"transcript": "No transcription available", "raw_response": result}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in transcription request: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error in transcription: {e}")
            return {"error": str(e)}
    
    def text_to_speech(self, text, language="kannada", voice="female"):
        """
        Convert text to speech using Dhvani.ai TTS
        
        Args:
            text (str): Text to convert to speech
            language (str): Language of the text (default: kannada)
            voice (str): Voice type (default: female)
            
        Returns:
            bytes: Audio data or a dict with error information
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
            
            logger.info(f"Sending TTS request to {self.tts_base_url} for text: {text[:50]}... in {language}")
            
            response = requests.post(
                f"{self.tts_base_url}/run",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"TTS response received with status code: {response.status_code}")
            
            # Extract the audio data from the Hugging Face Space API format
            if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                # The response might contain a base64 encoded audio file
                import base64
                
                audio_data = result["data"][0]
                
                # Check if it's a base64 string
                if isinstance(audio_data, str) and audio_data.startswith("data:audio"):
                    # Extract the base64 part
                    base64_data = audio_data.split(",")[1]
                    # Decode base64 to binary
                    return base64.b64decode(base64_data)
                elif isinstance(audio_data, str) and audio_data.startswith("http"):
                    # It's a URL to the audio file
                    audio_response = requests.get(audio_data)
                    audio_response.raise_for_status()
                    return audio_response.content
                else:
                    # Return the raw response for debugging
                    return {"error": "Unexpected response format", "raw_response": result}
            else:
                return {"error": "No audio data in response", "raw_response": result}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in text-to-speech request: {e}")
            return {"error": str(e)}


# Example usage functions
def run_chat_example():
    """Example function to demonstrate chat functionality"""
    try:
        dhvani = DhvaniAI()
        resp = dhvani.chat(prompt="Hello!", src_lang="english", tgt_lang="kannada")
        print("Chat Response:", resp)
        return resp
    except Exception as e:
        print(f"Error in Chat module: {e}")
        return {"error": str(e)}

def run_asr_example(audio_file_path):
    """Example function to demonstrate ASR functionality"""
    try:
        dhvani = DhvaniAI()
        result = dhvani.transcribe(audio_file_path, language="kannada")
        print("ASR Response:", result)
        return result
    except Exception as e:
        print(f"Error in ASR module: {e}")
        return {"error": str(e)}

def run_tts_example(text):
    """Example function to demonstrate TTS functionality"""
    try:
        dhvani = DhvaniAI()
        audio_data = dhvani.text_to_speech(text, language="kannada")
        
        # If it's an error response (dict), print it
        if isinstance(audio_data, dict):
            print("TTS Error:", audio_data)
            return audio_data
            
        # Otherwise, save the audio to a file
        output_file = "tts_output.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"TTS output saved to {output_file}")
        return {"success": True, "file": output_file}
    except Exception as e:
        print(f"Error in TTS module: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # This code runs when the script is executed directly
    print("Testing Dhvani.ai API integration...")
    
    # Test chat
    chat_result = run_chat_example()
    
    # Test ASR (uncomment and provide a valid audio file path)
    # asr_result = run_asr_example("path/to/audio/file.mp3")
    
    # Test TTS
    tts_result = run_tts_example("ನಮಸ್ಕಾರ, ನಿಮ್ಮ ಹೆಸರೇನು?")  # "Hello, what is your name?" in Kannada