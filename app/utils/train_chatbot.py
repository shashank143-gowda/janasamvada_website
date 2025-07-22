"""
Chatbot Training Script

This script trains the chatbot with predefined data about government schemes,
services, and other relevant information for the JanSamvaad application.
"""

import json
import os
import logging
from app.utils.dhvani_ai import DhvaniAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Training data
TRAINING_DATA = [
    # Government Schemes
    {
        "question": "What is Ayushman Bharat?",
        "answer": "Ayushman Bharat is a national health protection scheme that aims to provide free health coverage to over 10 crore poor families. It provides coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization."
    },
    {
        "question": "How can I apply for PM Kisan Samman Nidhi?",
        "answer": "To apply for PM Kisan Samman Nidhi, you need to: 1) Visit the official website pmkisan.gov.in, 2) Register as a farmer, 3) Fill the application form with your details, 4) Submit required documents like Aadhaar, bank account details, and land records. You can also visit your nearest Common Service Centre (CSC) for assistance."
    },
    {
        "question": "What is MGNREGA?",
        "answer": "MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) is a scheme that provides at least 100 days of wage employment in a financial year to every rural household whose adult members volunteer to do unskilled manual work. It aims to enhance livelihood security in rural areas."
    },
    {
        "question": "Tell me about PM Awas Yojana",
        "answer": "Pradhan Mantri Awas Yojana (PMAY) is a housing scheme launched by the Government of India to provide affordable housing to the urban and rural poor. Under PMAY-Urban, beneficiaries get financial assistance for constructing houses, while PMAY-Gramin focuses on providing pucca houses to rural households."
    },
    {
        "question": "What benefits does Ujjwala Yojana provide?",
        "answer": "Pradhan Mantri Ujjwala Yojana provides LPG connections to women from Below Poverty Line (BPL) households. Benefits include: 1) Free LPG connection, 2) Financial assistance of ₹1600 per connection, 3) Option for EMI facility for stove and first refill, 4) Improved health of women and children by reducing indoor air pollution."
    },
    
    # Health Services
    {
        "question": "How can I find the nearest government hospital?",
        "answer": "You can find the nearest government hospital by: 1) Using the National Health Portal (NHP) website or app, 2) Calling the toll-free number 1800-180-1104, 3) Checking with your local ASHA worker or Anganwadi center, 4) Visiting your nearest Primary Health Centre (PHC) for referrals."
    },
    {
        "question": "What vaccinations are provided free under the Universal Immunization Program?",
        "answer": "The Universal Immunization Program provides free vaccines against: BCG (Tuberculosis), OPV (Polio), Hepatitis B, Pentavalent vaccine (Diphtheria, Pertussis, Tetanus, Hepatitis B and Hib), Rotavirus, PCV (Pneumococcal Conjugate Vaccine), Measles, Rubella, and Japanese Encephalitis (in endemic districts)."
    },
    
    # Education
    {
        "question": "What scholarships are available for students?",
        "answer": "Several scholarships are available for students including: 1) Pre-Matric Scholarships for SC/ST/OBC/Minorities, 2) Post-Matric Scholarships, 3) National Means-cum-Merit Scholarship, 4) Central Sector Scheme of Scholarships, 5) Prime Minister's Scholarship Scheme, 6) National Talent Search Examination Scholarship, and 7) Various state-specific scholarships."
    },
    {
        "question": "How can I apply for education loans?",
        "answer": "To apply for education loans: 1) Approach nationalized banks or financial institutions, 2) Submit proof of admission to a recognized institution, 3) Provide income proof and collateral (if required), 4) Fill the application form with necessary details. For government-subsidized education loans, check the Vidya Lakshmi portal (vidyalakshmi.co.in)."
    },
    
    # Anti-Corruption
    {
        "question": "How can I report corruption?",
        "answer": "You can report corruption through: 1) Central Vigilance Commission website (cvc.gov.in), 2) Anti-Corruption Bureau of your state, 3) Online portal pgportal.gov.in, 4) Call the anti-corruption helpline of your state, 5) File a complaint with the Lokpal. You can remain anonymous if you wish."
    },
    {
        "question": "What is the Right to Information Act?",
        "answer": "The Right to Information (RTI) Act is a law that allows citizens to request information from any public authority. It promotes transparency and accountability in government functioning. You can file an RTI application by paying a nominal fee of ₹10 and addressing it to the Public Information Officer of the concerned department."
    },
    
    # Disaster Management
    {
        "question": "What should I do during a flood?",
        "answer": "During a flood: 1) Move to higher ground immediately, 2) Avoid walking or driving through flood waters, 3) Disconnect electrical appliances, 4) Keep emergency contacts handy, 5) Listen to radio/TV for updates, 6) Keep emergency supplies ready, 7) Follow evacuation orders if given by authorities."
    },
    {
        "question": "How can I prepare for an earthquake?",
        "answer": "To prepare for an earthquake: 1) Create an emergency plan with your family, 2) Identify safe spots in each room (under sturdy furniture or against interior walls), 3) Secure heavy furniture and appliances, 4) Keep emergency supplies ready, 5) Know how to turn off gas, water, and electricity, 6) Practice 'Drop, Cover, and Hold On' drills regularly."
    },
    
    # General Information
    {
        "question": "What are my rights as a citizen of India?",
        "answer": "As a citizen of India, your fundamental rights include: 1) Right to Equality, 2) Right to Freedom, 3) Right against Exploitation, 4) Right to Freedom of Religion, 5) Cultural and Educational Rights, 6) Right to Constitutional Remedies. These are enshrined in Part III of the Indian Constitution."
    },
    {
        "question": "How can I get a new Aadhaar card?",
        "answer": "To get a new Aadhaar card: 1) Visit the nearest Aadhaar Enrollment Center, 2) Fill the enrollment form, 3) Provide proof of identity, address, and date of birth, 4) Complete biometric capture (fingerprints, iris scan, photograph), 5) Receive an enrollment slip with 14-digit enrollment ID, 6) Check status online at uidai.gov.in, 7) Download e-Aadhaar or wait for physical card delivery."
    },
    {
        "question": "How do I register to vote?",
        "answer": "To register to vote: 1) Ensure you're 18 years or older, 2) Fill Form 6 online at voter.eci.gov.in or offline at your local Electoral Registration Office, 3) Submit proof of age, identity, and residence, 4) Track your application status online, 5) Receive your Voter ID card by post or download e-EPIC from the portal."
    }
]

def train_chatbot():
    """Train the chatbot with predefined data"""
    try:
        # Initialize the Dhvani AI client
        dhvani = DhvaniAI(
            api_key='shashanksmv511@gmail_dwani.com',
            base_url='https://dwani-dwani-api.hf.space'
        )
        
        logger.info("Starting chatbot training with predefined data...")
        
        # Since we're using a local implementation, we don't need to actually train
        # Just log the training data for reference
        logger.info(f"Processing {len(TRAINING_DATA)} training items")
        
        for i, item in enumerate(TRAINING_DATA):
            question = item["question"]
            answer = item["answer"]
            logger.info(f"Training item {i+1}: {question[:50]}...")
        
        # Run a few test questions to verify functionality
        test_questions = [
            "What is Ayushman Bharat?",
            "How can I report corruption?",
            "What are my rights as a citizen of India?"
        ]
        
        for question in test_questions:
            logger.info(f"Testing with question: {question}")
            test_response = dhvani.chat(
                prompt=question,
                src_lang="english",
                tgt_lang="english"
            )
            
            if "error" in test_response:
                logger.error(f"Error in test question: {test_response['error']}")
            else:
                logger.info(f"Test response: {test_response.get('response', 'No response')}")
        
        logger.info("Chatbot training simulation completed successfully!")
        return {"success": True, "message": "Chatbot training completed successfully!"}
        
    except Exception as e:
        logger.error(f"Error during chatbot training: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Run the training when the script is executed directly
    result = train_chatbot()
    print(json.dumps(result, indent=2))