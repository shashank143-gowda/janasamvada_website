"""
Fallback Responses for Chatbot

This module provides hardcoded responses for common questions
in case the API fails to respond properly.
"""

# Dictionary of fallback responses
FALLBACK_RESPONSES = {
    "ayushman bharat": "Ayushman Bharat is a national health protection scheme that aims to provide free health coverage to over 10 crore poor families. It provides coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization.",
    
    "pm kisan": "To apply for PM Kisan Samman Nidhi, you need to: 1) Visit the official website pmkisan.gov.in, 2) Register as a farmer, 3) Fill the application form with your details, 4) Submit required documents like Aadhaar, bank account details, and land records. You can also visit your nearest Common Service Centre (CSC) for assistance.",
    
    "mgnrega": "MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) is a scheme that provides at least 100 days of wage employment in a financial year to every rural household whose adult members volunteer to do unskilled manual work. It aims to enhance livelihood security in rural areas.",
    
    "awas yojana": "Pradhan Mantri Awas Yojana (PMAY) is a housing scheme launched by the Government of India to provide affordable housing to the urban and rural poor. Under PMAY-Urban, beneficiaries get financial assistance for constructing houses, while PMAY-Gramin focuses on providing pucca houses to rural households.",
    
    "ujjwala yojana": "Pradhan Mantri Ujjwala Yojana provides LPG connections to women from Below Poverty Line (BPL) households. Benefits include: 1) Free LPG connection, 2) Financial assistance of ₹1600 per connection, 3) Option for EMI facility for stove and first refill, 4) Improved health of women and children by reducing indoor air pollution.",
    
    "government hospital": "You can find the nearest government hospital by: 1) Using the National Health Portal (NHP) website or app, 2) Calling the toll-free number 1800-180-1104, 3) Checking with your local ASHA worker or Anganwadi center, 4) Visiting your nearest Primary Health Centre (PHC) for referrals.",
    
    "vaccination": "The Universal Immunization Program provides free vaccines against: BCG (Tuberculosis), OPV (Polio), Hepatitis B, Pentavalent vaccine (Diphtheria, Pertussis, Tetanus, Hepatitis B and Hib), Rotavirus, PCV (Pneumococcal Conjugate Vaccine), Measles, Rubella, and Japanese Encephalitis (in endemic districts).",
    
    "scholarship": "Several scholarships are available for students including: 1) Pre-Matric Scholarships for SC/ST/OBC/Minorities, 2) Post-Matric Scholarships, 3) National Means-cum-Merit Scholarship, 4) Central Sector Scheme of Scholarships, 5) Prime Minister's Scholarship Scheme, 6) National Talent Search Examination Scholarship, and 7) Various state-specific scholarships.",
    
    "education loan": "To apply for education loans: 1) Approach nationalized banks or financial institutions, 2) Submit proof of admission to a recognized institution, 3) Provide income proof and collateral (if required), 4) Fill the application form with necessary details. For government-subsidized education loans, check the Vidya Lakshmi portal (vidyalakshmi.co.in).",
    
    "corruption": "You can report corruption through: 1) Central Vigilance Commission website (cvc.gov.in), 2) Anti-Corruption Bureau of your state, 3) Online portal pgportal.gov.in, 4) Call the anti-corruption helpline of your state, 5) File a complaint with the Lokpal. You can remain anonymous if you wish.",
    
    "rti": "The Right to Information (RTI) Act is a law that allows citizens to request information from any public authority. It promotes transparency and accountability in government functioning. You can file an RTI application by paying a nominal fee of ₹10 and addressing it to the Public Information Officer of the concerned department.",
    
    "flood": "During a flood: 1) Move to higher ground immediately, 2) Avoid walking or driving through flood waters, 3) Disconnect electrical appliances, 4) Keep emergency contacts handy, 5) Listen to radio/TV for updates, 6) Keep emergency supplies ready, 7) Follow evacuation orders if given by authorities.",
    
    "earthquake": "To prepare for an earthquake: 1) Create an emergency plan with your family, 2) Identify safe spots in each room (under sturdy furniture or against interior walls), 3) Secure heavy furniture and appliances, 4) Keep emergency supplies ready, 5) Know how to turn off gas, water, and electricity, 6) Practice 'Drop, Cover, and Hold On' drills regularly.",
    
    "rights": "As a citizen of India, your fundamental rights include: 1) Right to Equality, 2) Right to Freedom, 3) Right against Exploitation, 4) Right to Freedom of Religion, 5) Cultural and Educational Rights, 6) Right to Constitutional Remedies. These are enshrined in Part III of the Indian Constitution.",
    
    "aadhaar": "To get a new Aadhaar card: 1) Visit the nearest Aadhaar Enrollment Center, 2) Fill the enrollment form, 3) Provide proof of identity, address, and date of birth, 4) Complete biometric capture (fingerprints, iris scan, photograph), 5) Receive an enrollment slip with 14-digit enrollment ID, 6) Check status online at uidai.gov.in, 7) Download e-Aadhaar or wait for physical card delivery.",
    
    "voter": "To register to vote: 1) Ensure you're 18 years or older, 2) Fill Form 6 online at voter.eci.gov.in or offline at your local Electoral Registration Office, 3) Submit proof of age, identity, and residence, 4) Track your application status online, 5) Receive your Voter ID card by post or download e-EPIC from the portal."
}

# Kannada translations of common responses
KANNADA_RESPONSES = {
    "ayushman bharat": "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಎನ್ನುವುದು ಬಡ ಕುಟುಂಬಗಳಿಗೆ ಉಚಿತ ಆರೋಗ್ಯ ರಕ್ಷಣೆಯನ್ನು ಒದಗಿಸುವ ರಾಷ್ಟ್ರೀಯ ಆರೋಗ್ಯ ರಕ್ಷಣಾ ಯೋಜನೆಯಾಗಿದೆ. ಇದು ಪ್ರತಿ ಕುಟುಂಬಕ್ಕೆ ಪ್ರತಿ ವರ್ಷ ₹5 ಲಕ್ಷದವರೆಗೆ ಮಾಧ್ಯಮಿಕ ಮತ್ತು ತೃತೀಯ ಆರೋಗ್ಯ ಸೇವೆಗಳಿಗೆ ರಕ್ಷಣೆ ನೀಡುತ್ತದೆ.",
    
    "pm kisan": "ಪಿಎಂ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು, ನೀವು: 1) ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ pmkisan.gov.in ಗೆ ಭೇಟಿ ನೀಡಿ, 2) ರೈತನಾಗಿ ನೋಂದಾಯಿಸಿಕೊಳ್ಳಿ, 3) ನಿಮ್ಮ ವಿವರಗಳೊಂದಿಗೆ ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ, 4) ಆಧಾರ್, ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು ಮತ್ತು ಭೂಮಿ ದಾಖಲೆಗಳಂತಹ ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ. ಸಹಾಯಕ್ಕಾಗಿ ನಿಮ್ಮ ಹತ್ತಿರದ ಕಾಮನ್ ಸರ್ವೀಸ್ ಸೆಂಟರ್ (CSC) ಗೆ ಭೇಟಿ ನೀಡಬಹುದು.",
    
    "mgnrega": "MGNREGA (ಮಹಾತ್ಮಾ ಗಾಂಧಿ ರಾಷ್ಟ್ರೀಯ ಗ್ರಾಮೀಣ ಉದ್ಯೋಗ ಖಾತರಿ ಕಾಯ್ದೆ) ಎನ್ನುವುದು ಅಕುಶಲ ದೈಹಿಕ ಕೆಲಸ ಮಾಡಲು ಸ್ವಯಂಪ್ರೇರಿತರಾಗಿರುವ ವಯಸ್ಕ ಸದಸ್ಯರನ್ನು ಹೊಂದಿರುವ ಪ್ರತಿ ಗ್ರಾಮೀಣ ಮನೆಗೆ ಹಣಕಾಸು ವರ್ಷದಲ್ಲಿ ಕನಿಷ್ಠ 100 ದಿನಗಳ ವೇತನ ಉದ್ಯೋಗವನ್ನು ಒದಗಿಸುವ ಯೋಜನೆಯಾಗಿದೆ. ಇದು ಗ್ರಾಮೀಣ ಪ್ರದೇಶಗಳಲ್ಲಿ ಜೀವನೋಪಾಯ ಭದ್ರತೆಯನ್ನು ಹೆಚ್ಚಿಸುವ ಗುರಿಯನ್ನು ಹೊಂದಿದೆ.",
    
    "awas yojana": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಆವಾಸ್ ಯೋಜನೆ (PMAY) ಎನ್ನುವುದು ನಗರ ಮತ್ತು ಗ್ರಾಮೀಣ ಬಡವರಿಗೆ ಕೈಗೆಟುಕುವ ವಸತಿ ಒದಗಿಸಲು ಭಾರತ ಸರ್ಕಾರ ಆರಂಭಿಸಿದ ವಸತಿ ಯೋಜನೆಯಾಗಿದೆ. PMAY-ಅರ್ಬನ್ ಅಡಿಯಲ್ಲಿ, ಫಲಾನುಭವಿಗಳು ಮನೆಗಳನ್ನು ನಿರ್ಮಿಸಲು ಹಣಕಾಸು ನೆರವು ಪಡೆಯುತ್ತಾರೆ, ಆದರೆ PMAY-ಗ್ರಾಮೀಣ ಗ್ರಾಮೀಣ ಮನೆಗಳಿಗೆ ಪಕ್ಕಾ ಮನೆಗಳನ್ನು ಒದಗಿಸುವ ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸುತ್ತದೆ.",
    
    "ujjwala yojana": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಉಜ್ವಲಾ ಯೋಜನೆಯು ಬಡತನ ರೇಖೆಗಿಂತ ಕೆಳಗಿರುವ (BPL) ಮನೆಗಳ ಮಹಿಳೆಯರಿಗೆ LPG ಸಂಪರ್ಕಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ. ಪ್ರಯೋಜನಗಳು: 1) ಉಚಿತ LPG ಸಂಪರ್ಕ, 2) ಪ್ರತಿ ಸಂಪರ್ಕಕ್ಕೆ ₹1600 ಹಣಕಾಸು ನೆರವು, 3) ಸ್ಟೋವ್ ಮತ್ತು ಮೊದಲ ಮರುಪೂರಣಕ್ಕಾಗಿ EMI ಸೌಲಭ್ಯದ ಆಯ್ಕೆ, 4) ಒಳಾಂಗಣ ವಾಯು ಮಾಲಿನ್ಯವನ್ನು ಕಡಿಮೆ ಮಾಡುವ ಮೂಲಕ ಮಹಿಳೆಯರು ಮತ್ತು ಮಕ್ಕಳ ಆರೋಗ್ಯದಲ್ಲಿ ಸುಧಾರಣೆ.",
    
    "government hospital": "ನೀವು ಹತ್ತಿರದ ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆಯನ್ನು ಹೀಗೆ ಕಂಡುಕೊಳ್ಳಬಹುದು: 1) ರಾಷ್ಟ್ರೀಯ ಆರೋಗ್ಯ ಪೋರ್ಟಲ್ (NHP) ವೆಬ್‌ಸೈಟ್ ಅಥವಾ ಅಪ್ಲಿಕೇಶನ್ ಬಳಸುವುದು, 2) ಟೋಲ್-ಫ್ರೀ ಸಂಖ್ಯೆ 1800-180-1104 ಗೆ ಕರೆ ಮಾಡುವುದು, 3) ನಿಮ್ಮ ಸ್ಥಳೀಯ ASHA ಕಾರ್ಯಕರ್ತ ಅಥವಾ ಅಂಗನವಾಡಿ ಕೇಂದ್ರದೊಂದಿಗೆ ಪರಿಶೀಲಿಸುವುದು, 4) ರೆಫರಲ್‌ಗಳಿಗಾಗಿ ನಿಮ್ಮ ಹತ್ತಿರದ ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರ (PHC) ಗೆ ಭೇಟಿ ನೀಡುವುದು.",
    
    "vaccination": "ಸಾರ್ವತ್ರಿಕ ಲಸಿಕಾ ಕಾರ್ಯಕ್ರಮವು ಈ ಕೆಳಗಿನವುಗಳ ವಿರುದ್ಧ ಉಚಿತ ಲಸಿಕೆಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ: BCG (ಕ್ಷಯರೋಗ), OPV (ಪೋಲಿಯೋ), ಹೆಪಟೈಟಿಸ್ B, ಪೆಂಟಾವಾಲೆಂಟ್ ಲಸಿಕೆ (ಡಿಫ್ತೀರಿಯಾ, ಪರ್ಟಸಿಸ್, ಟೆಟನಸ್, ಹೆಪಟೈಟಿಸ್ B ಮತ್ತು Hib), ರೋಟಾವೈರಸ್, PCV (ನ್ಯುಮೋಕಾಕಲ್ ಕಾಂಜುಗೇಟ್ ಲಸಿಕೆ), ಕಂದುರೋಗ, ರುಬೆಲ್ಲಾ ಮತ್ತು ಜಪಾನೀಸ್ ಎನ್ಸೆಫಲೈಟಿಸ್ (ಸ್ಥಳೀಯ ಜಿಲ್ಲೆಗಳಲ್ಲಿ).",
    
    "scholarship": "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಹಲವಾರು ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಲಭ್ಯವಿವೆ: 1) SC/ST/OBC/ಅಲ್ಪಸಂಖ್ಯಾತರಿಗೆ ಪ್ರಿ-ಮೆಟ್ರಿಕ್ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು, 2) ಪೋಸ್ಟ್-ಮೆಟ್ರಿಕ್ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು, 3) ರಾಷ್ಟ್ರೀಯ ಮೀನ್ಸ್-ಕಮ್-ಮೆರಿಟ್ ವಿದ್ಯಾರ್ಥಿವೇತನ, 4) ಕೇಂದ್ರ ವಲಯ ವಿದ್ಯಾರ್ಥಿವೇತನ ಯೋಜನೆ, 5) ಪ್ರಧಾನ ಮಂತ್ರಿ ವಿದ್ಯಾರ್ಥಿವೇತನ ಯೋಜನೆ, 6) ರಾಷ್ಟ್ರೀಯ ಪ್ರತಿಭಾ ಹುಡುಕಾಟ ಪರೀಕ್ಷಾ ವಿದ್ಯಾರ್ಥಿವೇತನ, ಮತ್ತು 7) ವಿವಿಧ ರಾಜ್ಯ-ನಿರ್ದಿಷ್ಟ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು.",
    
    "education loan": "ಶಿಕ್ಷಣ ಸಾಲಗಳಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು: 1) ರಾಷ್ಟ್ರೀಕೃತ ಬ್ಯಾಂಕುಗಳು ಅಥವಾ ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳನ್ನು ಸಂಪರ್ಕಿಸಿ, 2) ಮಾನ್ಯತೆ ಪಡೆದ ಸಂಸ್ಥೆಗೆ ಪ್ರವೇಶದ ಪುರಾವೆಯನ್ನು ಸಲ್ಲಿಸಿ, 3) ಆದಾಯದ ಪುರಾವೆ ಮತ್ತು ಜಾಮೀನು (ಅಗತ್ಯವಿದ್ದರೆ) ಒದಗಿಸಿ, 4) ಅಗತ್ಯ ವಿವರಗಳೊಂದಿಗೆ ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ. ಸರ್ಕಾರದಿಂದ ಸಬ್ಸಿಡಿ ನೀಡಲಾದ ಶಿಕ್ಷಣ ಸಾಲಗಳಿಗಾಗಿ, ವಿದ್ಯಾ ಲಕ್ಷ್ಮಿ ಪೋರ್ಟಲ್ (vidyalakshmi.co.in) ಅನ್ನು ಪರಿಶೀಲಿಸಿ.",
    
    "corruption": "ನೀವು ಭ್ರಷ್ಟಾಚಾರವನ್ನು ಹೀಗೆ ವರದಿ ಮಾಡಬಹುದು: 1) ಕೇಂದ್ರ ಜಾಗೃತಾ ಆಯೋಗದ ವೆಬ್‌ಸೈಟ್ (cvc.gov.in), 2) ನಿಮ್ಮ ರಾಜ್ಯದ ಭ್ರಷ್ಟಾಚಾರ ನಿಗ್ರಹ ದಳ, 3) ಆನ್‌ಲೈನ್ ಪೋರ್ಟಲ್ pgportal.gov.in, 4) ನಿಮ್ಮ ರಾಜ್ಯದ ಭ್ರಷ್ಟಾಚಾರ ವಿರೋಧಿ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ, 5) ಲೋಕಪಾಲ್‌ಗೆ ದೂರು ಸಲ್ಲಿಸಿ. ನೀವು ಬಯಸಿದರೆ ಅನಾಮಧೇಯರಾಗಿ ಉಳಿಯಬಹುದು.",
    
    "rti": "ಮಾಹಿತಿ ಹಕ್ಕು (RTI) ಕಾಯ್ದೆಯು ನಾಗರಿಕರು ಯಾವುದೇ ಸಾರ್ವಜನಿಕ ಪ್ರಾಧಿಕಾರದಿಂದ ಮಾಹಿತಿಯನ್ನು ಕೋರಲು ಅನುವು ಮಾಡಿಕೊಡುವ ಕಾನೂನಾಗಿದೆ. ಇದು ಸರ್ಕಾರಿ ಕಾರ್ಯನಿರ್ವಹಣೆಯಲ್ಲಿ ಪಾರದರ್ಶಕತೆ ಮತ್ತು ಜವಾಬ್ದಾರಿಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ. ನೀವು ₹10 ರ ಸಾಂಕೇತಿಕ ಶುಲ್ಕವನ್ನು ಪಾವತಿಸುವ ಮೂಲಕ ಮತ್ತು ಸಂಬಂಧಿತ ಇಲಾಖೆಯ ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ಅಧಿಕಾರಿಗೆ ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಬಹುದು.",
    
    "flood": "ಪ್ರವಾಹದ ಸಮಯದಲ್ಲಿ: 1) ತಕ್ಷಣವೇ ಎತ್ತರದ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ, 2) ಪ್ರವಾಹದ ನೀರಿನ ಮೂಲಕ ನಡೆಯುವುದನ್ನು ಅಥವಾ ಚಾಲನೆ ಮಾಡುವುದನ್ನು ತಪ್ಪಿಸಿ, 3) ವಿದ್ಯುತ್ ಉಪಕರಣಗಳನ್ನು ಸಂಪರ್ಕ ಕಡಿತಗೊಳಿಸಿ, 4) ತುರ್ತು ಸಂಪರ್ಕಗಳನ್ನು ಸಿದ್ಧವಾಗಿರಿಸಿ, 5) ನವೀಕರಣಗಳಿಗಾಗಿ ರೇಡಿಯೋ/ಟಿವಿ ಆಲಿಸಿ, 6) ತುರ್ತು ಸರಬರಾಜುಗಳನ್ನು ಸಿದ್ಧವಾಗಿರಿಸಿ, 7) ಅಧಿಕಾರಿಗಳು ನೀಡಿದ ಸ್ಥಳಾಂತರ ಆದೇಶಗಳನ್ನು ಅನುಸರಿಸಿ.",
    
    "earthquake": "ಭೂಕಂಪಕ್ಕೆ ಸಿದ್ಧತೆ ಮಾಡಿಕೊಳ್ಳಲು: 1) ನಿಮ್ಮ ಕುಟುಂಬದೊಂದಿಗೆ ತುರ್ತು ಯೋಜನೆಯನ್ನು ರಚಿಸಿ, 2) ಪ್ರತಿ ಕೋಣೆಯಲ್ಲಿ ಸುರಕ್ಷಿತ ಸ್ಥಳಗಳನ್ನು ಗುರುತಿಸಿ (ಗಟ್ಟಿಯಾದ ಫರ್ನಿಚರ್ ಅಡಿಯಲ್ಲಿ ಅಥವಾ ಒಳಗಿನ ಗೋಡೆಗಳ ಎದುರು), 3) ಭಾರೀ ಫರ್ನಿಚರ್ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸುರಕ್ಷಿತಗೊಳಿಸಿ, 4) ತುರ್ತು ಸರಬರಾಜುಗಳನ್ನು ಸಿದ್ಧವಾಗಿರಿಸಿ, 5) ಗ್ಯಾಸ್, ನೀರು ಮತ್ತು ವಿದ್ಯುತ್ ಅನ್ನು ಹೇಗೆ ಆಫ್ ಮಾಡಬೇಕೆಂದು ತಿಳಿದುಕೊಳ್ಳಿ, 6) ನಿಯಮಿತವಾಗಿ 'ಕುಸಿಯಿರಿ, ಮುಚ್ಚಿಕೊಳ್ಳಿ ಮತ್ತು ಹಿಡಿದುಕೊಳ್ಳಿ' ಅಭ್ಯಾಸಗಳನ್ನು ಮಾಡಿ.",
    
    "rights": "ಭಾರತದ ನಾಗರಿಕನಾಗಿ, ನಿಮ್ಮ ಮೂಲಭೂತ ಹಕ್ಕುಗಳು: 1) ಸಮಾನತೆಯ ಹಕ್ಕು, 2) ಸ್ವಾತಂತ್ರ್ಯದ ಹಕ್ಕು, 3) ಶೋಷಣೆಯ ವಿರುದ್ಧದ ಹಕ್ಕು, 4) ಧಾರ್ಮಿಕ ಸ್ವಾತಂತ್ರ್ಯದ ಹಕ್ಕು, 5) ಸಾಂಸ್ಕೃತಿಕ ಮತ್ತು ಶೈಕ್ಷಣಿಕ ಹಕ್ಕುಗಳು, 6) ಸಾಂವಿಧಾನಿಕ ಪರಿಹಾರಗಳ ಹಕ್ಕು. ಇವುಗಳನ್ನು ಭಾರತೀಯ ಸಂವಿಧಾನದ ಭಾಗ III ರಲ್ಲಿ ಸೇರಿಸಲಾಗಿದೆ.",
    
    "aadhaar": "ಹೊಸ ಆಧಾರ್ ಕಾರ್ಡ್ ಪಡೆಯಲು: 1) ಹತ್ತಿರದ ಆಧಾರ್ ನೋಂದಣಿ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ, 2) ನೋಂದಣಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ, 3) ಗುರುತಿನ ಪುರಾವೆ, ವಿಳಾಸ ಮತ್ತು ಜನ್ಮ ದಿನಾಂಕದ ಪುರಾವೆಯನ್ನು ಒದಗಿಸಿ, 4) ಬಯೋಮೆಟ್ರಿಕ್ ಸೆರೆಹಿಡಿಯುವಿಕೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ (ಬೆರಳಚ್ಚುಗಳು, ಕಣ್ಣಿನ ಗುಡ್ಡೆಯ ಸ್ಕ್ಯಾನ್, ಫೋಟೋಗ್ರಾಫ್), 5) 14-ಅಂಕಿಯ ನೋಂದಣಿ ID ಯೊಂದಿಗೆ ನೋಂದಣಿ ಸ್ಲಿಪ್ ಪಡೆಯಿರಿ, 6) uidai.gov.in ನಲ್ಲಿ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ, 7) e-ಆಧಾರ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಭೌತಿಕ ಕಾರ್ಡ್ ವಿತರಣೆಗಾಗಿ ಕಾಯಿರಿ.",
    
    "voter": "ಮತದಾನಕ್ಕೆ ನೋಂದಾಯಿಸಲು: 1) ನೀವು 18 ವರ್ಷ ಅಥವಾ ಅದಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ವಯಸ್ಸಿನವರಾಗಿದ್ದೀರಿ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ, 2) voter.eci.gov.in ನಲ್ಲಿ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅಥವಾ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಚುನಾವಣಾ ನೋಂದಣಿ ಕಚೇರಿಯಲ್ಲಿ ಆಫ್‌ಲೈನ್‌ನಲ್ಲಿ ನಮೂನೆ 6 ಅನ್ನು ಭರ್ತಿ ಮಾಡಿ, 3) ವಯಸ್ಸು, ಗುರುತು ಮತ್ತು ನಿವಾಸದ ಪುರಾವೆಯನ್ನು ಸಲ್ಲಿಸಿ, 4) ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ನಿಮ್ಮ ಅರ್ಜಿಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ, 5) ನಿಮ್ಮ ಮತದಾರರ ID ಕಾರ್ಡ್ ಅನ್ನು ಅಂಚೆ ಮೂಲಕ ಪಡೆಯಿರಿ ಅಥವಾ ಪೋರ್ಟಲ್‌ನಿಂದ e-EPIC ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ."
}

def get_fallback_response(query, language='en'):
    """
    Get a fallback response for a query
    
    Args:
        query (str): The user's query
        language (str): The language code ('en' or 'kn')
        
    Returns:
        str: A fallback response if available, None otherwise
    """
    query = query.lower()
    
    # Use the appropriate response dictionary based on language
    responses = KANNADA_RESPONSES if language == 'kn' else FALLBACK_RESPONSES
    
    # Check for exact matches first
    if query in responses:
        return responses[query]
    
    # Check for partial matches
    for key, response in responses.items():
        if key in query:
            return response
    
    # Default response if no match found
    return None