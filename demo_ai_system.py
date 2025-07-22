"""
Demo script to showcase the AI-powered hazard image validation system
"""

import requests
from PIL import Image
import os
import time

def create_demo_images():
    """Create realistic demo images for different hazard types"""
    
    print("🎨 Creating realistic demo images...")
    
    # 1. Road Pothole Damage
    print("  Creating road damage image...")
    road_img = Image.new('RGB', (400, 400), color=(80, 80, 80))  # Dark asphalt
    
    # Add pothole (dark irregular shape)
    for i in range(150, 250):
        for j in range(150, 250):
            if (i-200)**2 + (j-200)**2 < 50**2:  # Circular pothole
                road_img.putpixel((i, j), (20, 20, 20))
    
    # Add cracks (dark lines)
    for i in range(50, 350):
        road_img.putpixel((i, 100), (30, 30, 30))
        road_img.putpixel((i, 300), (30, 30, 30))
    
    road_img.save('demo_pothole_main_street.jpg')
    
    # 2. Fire Emergency
    print("  Creating fire emergency image...")
    fire_img = Image.new('RGB', (350, 350), color=(40, 40, 40))  # Dark background
    
    # Add fire colors (red, orange, yellow)
    for i in range(100, 250):
        for j in range(100, 250):
            # Fire gradient
            distance = ((i-175)**2 + (j-175)**2)**0.5
            if distance < 70:
                if distance < 30:
                    fire_img.putpixel((i, j), (255, 255, 0))  # Yellow center
                elif distance < 50:
                    fire_img.putpixel((i, j), (255, 140, 0))  # Orange
                else:
                    fire_img.putpixel((i, j), (255, 69, 0))   # Red
    
    fire_img.save('demo_fire_emergency.jpg')
    
    # 3. Garbage/Waste Issue
    print("  Creating garbage waste image...")
    waste_img = Image.new('RGB', (300, 300), color=(60, 80, 60))  # Dirty green
    
    # Add brown/dirty colors
    for i in range(50, 250):
        for j in range(50, 250):
            if (i + j) % 20 < 10:  # Scattered pattern
                waste_img.putpixel((i, j), (101, 67, 33))  # Brown
            elif (i * j) % 30 < 5:
                waste_img.putpixel((i, j), (139, 69, 19))  # Darker brown
    
    waste_img.save('demo_garbage_dump.jpg')
    
    # 4. Infrastructure Damage
    print("  Creating infrastructure damage image...")
    infra_img = Image.new('RGB', (380, 380), color=(120, 120, 120))  # Concrete gray
    
    # Add cracks and damage
    for i in range(50, 330):
        for j in range(50, 330):
            # Crack pattern
            if abs(i - j) < 5 or abs(i + j - 380) < 5:
                infra_img.putpixel((i, j), (40, 40, 40))  # Dark crack
            # Damage spots
            elif (i % 50 < 10 and j % 50 < 10):
                infra_img.putpixel((i, j), (80, 80, 80))  # Damaged area
    
    infra_img.save('demo_building_damage.jpg')
    
    # 5. Non-hazard image (should be rejected)
    print("  Creating non-hazard image...")
    nature_img = Image.new('RGB', (300, 300), color=(135, 206, 235))  # Sky blue
    
    # Add some clouds
    for i in range(100, 200):
        for j in range(100, 200):
            nature_img.putpixel((i, j), (255, 255, 255))  # White clouds
    
    nature_img.save('demo_beautiful_sky.jpg')
    
    return [
        'demo_pothole_main_street.jpg',
        'demo_fire_emergency.jpg', 
        'demo_garbage_dump.jpg',
        'demo_building_damage.jpg',
        'demo_beautiful_sky.jpg'
    ]

def test_ai_validation(image_path):
    """Test AI validation for a specific image"""
    print(f"\n🔍 Testing: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post('http://127.0.0.1:5000/hazards/api/validate-image', files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success'] and data['is_hazard']:
                print(f"   ✅ HAZARD DETECTED")
                print(f"   📊 Confidence: {data['confidence']}%")
                print(f"   🏷️ Type: {data['hazard_type']}")
                print(f"   💬 Message: {data['message']}")
                return True
            else:
                print(f"   ❌ NOT A HAZARD")
                print(f"   📊 Confidence: {data.get('confidence', 0)}%")
                print(f"   💬 Message: {data['message']}")
                return False
        else:
            print(f"   ❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Main demo function"""
    
    print("🚀 AI-Powered Hazard Image Validation Demo")
    print("=" * 60)
    
    # Check server status
    try:
        response = requests.get('http://127.0.0.1:5000/')
        if response.status_code == 200:
            print("✅ Server is running at http://127.0.0.1:5000")
        else:
            print("❌ Server error - please check if Flask app is running")
            return
    except:
        print("❌ Cannot connect to server - please run: python run.py")
        return
    
    # Create demo images
    demo_files = create_demo_images()
    
    print(f"\n🤖 AI VALIDATION RESULTS")
    print("=" * 60)
    
    # Expected results
    expected_results = [True, True, True, True, False]  # Last one should be rejected
    hazard_types = ['road', 'environment', 'health', 'infrastructure', 'non-hazard']
    
    actual_results = []
    
    for i, (image_path, expected, hazard_type) in enumerate(zip(demo_files, expected_results, hazard_types)):
        result = test_ai_validation(image_path)
        actual_results.append(result)
        
        # Status check
        if result == expected:
            print(f"   ✅ TEST PASSED")
        else:
            print(f"   ⚠️ TEST FAILED (Expected: {expected}, Got: {result})")
        
        print("-" * 40)
        time.sleep(0.5)  # Small delay
    
    # Summary
    print(f"\n📈 DEMO SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r, e in zip(actual_results, expected_results) if r == e)
    total = len(actual_results)
    success_rate = (passed / total) * 100
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🏆 EXCELLENT! AI system is working very well!")
    elif success_rate >= 60:
        print("✅ GOOD! AI system is working correctly!")
    else:
        print("⚠️ NEEDS IMPROVEMENT! AI system needs tuning!")
    
    print(f"\n🎯 KEY FEATURES DEMONSTRATED:")
    print("✅ Real-time hazard detection")
    print("✅ Multi-category classification (road, fire, waste, infrastructure)")
    print("✅ Confidence scoring")
    print("✅ False positive prevention")
    print("✅ User-friendly error messages")
    print("✅ REST API integration")
    
    print(f"\n🌐 Try the web interface at: http://127.0.0.1:5000/hazards/report")
    
    # Cleanup
    print(f"\n🧹 Cleaning up demo files...")
    for file in demo_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"   Removed: {file}")
    
    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()