from app import create_app
from app.models.models import db, User, PublicService, GovernmentScheme, ClimateInfo
from datetime import datetime, timedelta
import random

app = create_app()

def init_db():
    with app.app_context():
        # Create tables
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@jansamvaad.org',
            phone='9876543210',
            village='Admin Village',
            district='Admin District',
            state='Admin State',
            reward_points=1000
        )
        admin.set_password('admin1234')
       
        
        db.session.add(admin)
       
        
        # Add public services
        services = [
            PublicService(
                name='District Hospital',
                service_type='hospital',
                address='Main Road, Ranchi',
                contact='0651-2222222',
                latitude=23.3441,
                longitude=85.3096,
                district='Ranchi',
                state='Jharkhand'
            ),
            PublicService(
                name='Primary Health Center',
                service_type='hospital',
                address='Village Road, Sundarpur',
                contact='0651-3333333',
                latitude=23.3541,
                longitude=85.3196,
                district='Ranchi',
                state='Jharkhand'
            ),
            PublicService(
                name='Government High School',
                service_type='school',
                address='Education Lane, Ranchi',
                contact='0651-4444444',
                latitude=23.3641,
                longitude=85.3296,
                district='Ranchi',
                state='Jharkhand'
            ),
            PublicService(
                name='Bus Station',
                service_type='transport',
                address='Transport Nagar, Ranchi',
                contact='0651-5555555',
                latitude=23.3741,
                longitude=85.3396,
                district='Ranchi',
                state='Jharkhand'
            ),
            PublicService(
                name='Agricultural Extension Office',
                service_type='agriculture',
                address='Farm Road, Ranchi',
                contact='0651-6666666',
                latitude=23.3841,
                longitude=85.3496,
                district='Ranchi',
                state='Jharkhand'
            )
        ]
        
        for service in services:
            db.session.add(service)
        
        # Add government schemes
        schemes = [
            GovernmentScheme(
                name='PM Kisan Samman Nidhi',
                category='agriculture',
                description='Direct income support of Rs. 6000 per year to farmer families',
                eligibility='All small and marginal farmers with cultivable land',
                application_process='1. Register on PM Kisan portal\n2. Submit land records\n3. Link Aadhaar and bank account',
                documents_required='Aadhaar Card, Land Records, Bank Passbook',
                contact_info='Toll Free: 1800-11-0001',
                website='https://pmkisan.gov.in/'
            ),
            GovernmentScheme(
                name='Ayushman Bharat',
                category='health',
                description='Health insurance coverage of Rs. 5 lakh per family per year',
                eligibility='Economically weaker sections as per SECC database',
                application_process='1. Check eligibility on website\n2. Visit nearest Ayushman Mitra\n3. Get e-card issued',
                documents_required='Aadhaar Card, Ration Card, Income Certificate',
                contact_info='Toll Free: 14555',
                website='https://pmjay.gov.in/'
            ),
            GovernmentScheme(
                name='PM Awas Yojana (Rural)',
                category='housing',
                description='Financial assistance for construction of pucca house',
                eligibility='Houseless people and those living in dilapidated houses',
                application_process='1. Apply through Gram Panchayat\n2. Get house sanctioned\n3. Receive installments based on construction progress',
                documents_required='Aadhaar Card, Land Documents, BPL Card',
                contact_info='Contact local Gram Panchayat',
                website='https://pmayg.nic.in/'
            ),
            GovernmentScheme(
                name='Sukanya Samriddhi Yojana',
                category='women',
                description='Small savings scheme for girl child with high interest rate',
                eligibility='Parents of girl child below 10 years',
                application_process='1. Open account in post office or bank\n2. Deposit minimum Rs. 250 per year\n3. Maturity after 21 years',
                documents_required='Birth Certificate of Girl Child, ID proof of parents',
                contact_info='Contact local post office or bank',
                website='https://www.india.gov.in/sukanya-samriddhi-account'
            ),
            GovernmentScheme(
                name='PM Ujjwala Yojana',
                category='energy',
                description='Free LPG connections to women from BPL households',
                eligibility='Women from BPL households without LPG connection',
                application_process='1. Submit application to LPG distributor\n2. Get connection installed\n3. Receive subsidy in bank account',
                documents_required='Aadhaar Card, BPL Certificate, Bank Account details',
                contact_info='Toll Free: 1800-266-6696',
                website='https://pmuy.gov.in/'
            )
        ]
        
        for scheme in schemes:
            db.session.add(scheme)
        
        # Add climate information
        today = datetime.now().date()
        
        weather_conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain']
        regions = ['Ranchi', 'Hazaribagh', 'Dhanbad', 'Jamshedpur']
        
        for i in range(7):  # Add data for next 7 days
            date = today + timedelta(days=i)
            
            for region in regions:
                weather_condition = random.choice(weather_conditions)
                temperature = round(random.uniform(22.0, 35.0), 1)
                
                if weather_condition == 'Sunny':
                    rainfall = 'No rainfall expected'
                    farming_tip = 'Good day for harvesting crops. Ensure proper hydration for plants.'
                elif weather_condition == 'Partly Cloudy':
                    rainfall = 'Low chance of light showers'
                    farming_tip = 'Moderate conditions for field work. Good time for planting.'
                elif weather_condition == 'Cloudy':
                    rainfall = 'Moderate chance of rainfall'
                    farming_tip = 'Consider covering sensitive crops. Good time for planting.'
                elif weather_condition == 'Light Rain':
                    rainfall = 'Light rainfall expected'
                    farming_tip = 'Good day for planting. Avoid applying fertilizers.'
                else:  # Heavy Rain
                    rainfall = 'Heavy rainfall expected'
                    farming_tip = 'Avoid field work. Ensure proper drainage in fields.'
                
                climate_info = ClimateInfo(
                    date=date,
                    temperature=temperature,
                    weather_condition=weather_condition,
                    rainfall_prediction=rainfall,
                    farming_tip=farming_tip,
                    region=region
                )
                
                db.session.add(climate_info)
        
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db()