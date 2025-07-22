"""
Test script for the hazard image classifier
"""

import sys
import os
sys.path.append('.')

from app.utils.hazard_image_classifier import validate_hazard_image

def test_classifier():
    print("Testing Hazard Image Classifier...")
    
    # Test with a sample image (we'll just test that it doesn't crash)
    try:
        # Create a test image
        from PIL import Image
        
        # Create a test image with dark patches (simulating a pothole)
        test_image = Image.new('RGB', (300, 300), color='gray')
        
        # Add some dark patches
        for i in range(50, 150):
            for j in range(50, 150):
                test_image.putpixel((i, j), (30, 30, 30))  # Dark patch
        
        # Save test image
        test_path = 'test_hazard_image.jpg'
        test_image.save(test_path)
        
        # Test the classifier
        is_valid, confidence, hazard_type, message = validate_hazard_image(test_path)
        
        print(f"✓ Test completed successfully!")
        print(f"  - Valid: {is_valid}")
        print(f"  - Confidence: {confidence:.2f}%")
        print(f"  - Hazard Type: {hazard_type}")
        print(f"  - Message: {message}")
        
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)
            
        return True
        
    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_classifier()
    sys.exit(0 if success else 1)