"""
Advanced test for the hazard image classifier
"""

import sys
import os
sys.path.append('.')

from app.utils.hazard_image_classifier import validate_hazard_image
from PIL import Image

def test_hazard_detection():
    print("Testing Advanced Hazard Detection...")
    
    # Test 1: Create an image with many dark patches (simulating road damage)
    print("\n1. Testing road damage simulation...")
    test_image = Image.new('RGB', (400, 400), color='gray')
    
    # Add many dark patches and high contrast areas
    for i in range(0, 400, 30):
        for j in range(0, 400, 30):
            # Dark patches
            for x in range(i, min(i+15, 400)):
                for y in range(j, min(j+15, 400)):
                    test_image.putpixel((x, y), (20, 20, 20))
    
    test_path = 'test_road_damage.jpg'
    test_image.save(test_path)
    
    is_valid, confidence, hazard_type, message = validate_hazard_image(test_path)
    print(f"  - Valid: {is_valid} | Confidence: {confidence:.2f}% | Type: {hazard_type}")
    
    # Test 2: Create an image with filename hint
    print("\n2. Testing filename-based detection...")
    test_path2 = 'pothole_main_street.jpg'
    test_image.save(test_path2)
    
    is_valid2, confidence2, hazard_type2, message2 = validate_hazard_image(test_path2)
    print(f"  - Valid: {is_valid2} | Confidence: {confidence2:.2f}% | Type: {hazard_type2}")
    
    # Test 3: Create an image with red colors (fire simulation)
    print("\n3. Testing fire/red color detection...")
    red_image = Image.new('RGB', (300, 300), color=(200, 50, 50))
    test_path3 = 'fire_hazard.jpg'
    red_image.save(test_path3)
    
    is_valid3, confidence3, hazard_type3, message3 = validate_hazard_image(test_path3)
    print(f"  - Valid: {is_valid3} | Confidence: {confidence3:.2f}% | Type: {hazard_type3}")
    
    # Clean up
    for path in [test_path, test_path2, test_path3]:
        if os.path.exists(path):
            os.remove(path)
    
    print(f"\n✓ Advanced testing completed!")
    return True

if __name__ == "__main__":
    test_hazard_detection()