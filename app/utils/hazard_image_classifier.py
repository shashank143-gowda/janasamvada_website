"""
AI-based Image Classification for Hazard Detection
This module provides intelligent image classification to determine if uploaded images
are related to hazards like road damage, infrastructure issues, environmental hazards, etc.
"""

from PIL import Image
import os
import logging
import colorsys
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HazardImageClassifier:
    def __init__(self):
        """Initialize the hazard image classifier with heuristic-based analysis"""
        self.hazard_keywords = {
            # Road hazards
            'road_hazards': [
                'road', 'pothole', 'crack', 'asphalt', 'pavement', 'street', 'highway',
                'traffic', 'damaged road', 'broken road', 'road damage', 'street damage'
            ],
            
            # Infrastructure hazards
            'infrastructure_hazards': [
                'building', 'bridge', 'construction', 'broken', 'damaged building',
                'collapsed', 'crack', 'structure', 'concrete', 'wall', 'pillar',
                'damaged bridge', 'unsafe building', 'broken infrastructure'
            ],
            
            # Environmental hazards
            'environmental_hazards': [
                'flood', 'water', 'tree', 'fallen tree', 'fire', 'smoke', 'pollution',
                'garbage', 'waste', 'sewage', 'overflow', 'environmental damage',
                'natural disaster', 'landslide', 'erosion'
            ],
            
            # Public safety hazards
            'public_safety_hazards': [
                'unsafe', 'dangerous', 'accident', 'hazard', 'warning', 'danger',
                'safety issue', 'public danger', 'unsafe area', 'security risk'
            ],
            
            # Health hazards
            'health_hazards': [
                'sewage', 'waste', 'garbage', 'contamination', 'leak', 'spill',
                'toxic', 'health risk', 'sanitation', 'pollution', 'unhygienic'
            ]
        }
        
        logger.info("Hazard image classifier initialized with heuristic analysis")
    
    def is_hazard_related(self, image_path):
        """
        Determine if the image is related to a hazard using visual analysis
        Returns: (is_hazard: bool, confidence: float, predicted_class: str, reason: str)
        """
        try:
            # Perform visual analysis
            visual_score = self.analyze_visual_features(image_path)
            
            # Perform filename analysis
            filename_score = self.analyze_filename(image_path)
            
            # Perform color analysis
            color_score = self.analyze_colors(image_path)
            
            # Perform texture analysis
            texture_score = self.analyze_texture(image_path)
            
            # Combine all scores
            total_score = visual_score + filename_score + color_score + texture_score
            
            # Determine hazard type based on analysis
            hazard_type = self.determine_hazard_type(image_path, visual_score, color_score, texture_score)
            
            # Determine if it's a hazard (threshold: 35%)
            is_hazard = total_score > 35
            
            confidence = min(total_score, 100)
            
            if is_hazard:
                reason = f"Detected potential hazard indicators (score: {total_score:.1f})"
            else:
                reason = "No significant hazard indicators detected in the image"
            
            logger.info(f"Image analysis result: hazard={is_hazard}, confidence={confidence:.2f}%, type={hazard_type}")
            
            return is_hazard, confidence, hazard_type, reason
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            # In case of error, allow the upload (fail-safe)
            return True, 50.0, "unknown", f"Error during analysis: {str(e)}"
    
    def analyze_visual_features(self, image_path):
        """
        Analyze visual features that might indicate hazards
        Returns confidence score (0-100)
        """
        try:
            image = Image.open(image_path)
            image = image.convert('RGB')
            
            # Convert to grayscale for analysis
            gray = image.convert('L')
            
            # Get image statistics
            width, height = image.size
            pixels = list(gray.getdata())
            
            score = 0
            
            # Check for dark areas (potential potholes, cracks, damage)
            dark_pixels = sum(1 for p in pixels if p < 50)
            dark_ratio = dark_pixels / len(pixels)
            if dark_ratio > 0.1:  # More than 10% dark areas
                score += 25
            
            # Check for high contrast (potential damage, cracks)
            pixel_variance = statistics.variance(pixels) if len(pixels) > 1 else 0
            if pixel_variance > 3000:  # High variance indicates irregular patterns
                score += 15
            
            # Check for edge density (damaged surfaces have more edges)
            edge_score = self.calculate_edge_density(gray)
            if edge_score > 0.3:
                score += 10
            
            return score
            
        except Exception as e:
            logger.error(f"Error in visual feature analysis: {str(e)}")
            return 0
    
    def analyze_filename(self, image_path):
        """
        Analyze filename for hazard-related keywords
        Returns confidence score (0-100)
        """
        try:
            filename = os.path.basename(image_path).lower()
            
            # Common hazard-related terms in filenames
            hazard_terms = [
                'pothole', 'crack', 'damage', 'broken', 'fire', 'flood',
                'garbage', 'waste', 'hazard', 'danger', 'accident',
                'repair', 'construction', 'road', 'street', 'bridge',
                'building', 'infrastructure', 'leak', 'spill', 'pollution'
            ]
            
            score = 0
            for term in hazard_terms:
                if term in filename:
                    score += 10
                    
            return min(score, 25)  # Cap at 25 points
            
        except Exception as e:
            logger.error(f"Error in filename analysis: {str(e)}")
            return 0
    
    def analyze_colors(self, image_path):
        """
        Analyze color distribution for hazard indicators
        Returns confidence score (0-100)
        """
        try:
            image = Image.open(image_path)
            image = image.convert('RGB')
            
            # Sample pixels for color analysis
            pixels = list(image.getdata())
            
            score = 0
            
            # Count different color types
            dark_count = 0
            brown_count = 0
            red_count = 0
            gray_count = 0
            
            for r, g, b in pixels[::100]:  # Sample every 100th pixel
                # Convert to HSV for better color analysis
                h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                
                # Check for dark colors (potential damage)
                if v < 0.3:
                    dark_count += 1
                
                # Check for brown colors (dirt, mud, road damage)
                if 0.05 < h < 0.15 and s > 0.3:
                    brown_count += 1
                
                # Check for red colors (fire, danger signs)
                if (h < 0.05 or h > 0.95) and s > 0.5:
                    red_count += 1
                
                # Check for gray colors (concrete, asphalt)
                if s < 0.2 and 0.3 < v < 0.7:
                    gray_count += 1
            
            total_samples = len(pixels) // 100
            
            # Score based on color distribution
            if dark_count / total_samples > 0.3:
                score += 15
            if brown_count / total_samples > 0.2:
                score += 10
            if red_count / total_samples > 0.1:
                score += 25  # Higher score for red (fire, emergency)
            if gray_count / total_samples > 0.4:
                score += 10
            
            # Additional scoring for fire-like colors
            orange_count = 0
            for r, g, b in pixels[::100]:
                if r > 200 and g > 80 and g < 150 and b < 100:  # Orange/fire colors
                    orange_count += 1
            
            if orange_count / total_samples > 0.15:
                score += 20
            
            return score
            
        except Exception as e:
            logger.error(f"Error in color analysis: {str(e)}")
            return 0
    
    def analyze_texture(self, image_path):
        """
        Analyze texture patterns for hazard indicators
        Returns confidence score (0-100)
        """
        try:
            image = Image.open(image_path)
            gray = image.convert('L')
            
            # Simple texture analysis based on local variance
            width, height = gray.size
            pixels = list(gray.getdata())
            
            score = 0
            
            # Check for texture irregularities (potential damage)
            if width > 100 and height > 100:
                # Sample 3x3 blocks and check variance
                high_variance_blocks = 0
                total_blocks = 0
                
                for y in range(0, height - 3, 20):
                    for x in range(0, width - 3, 20):
                        block = []
                        for dy in range(3):
                            for dx in range(3):
                                if (y + dy) * width + (x + dx) < len(pixels):
                                    block.append(pixels[(y + dy) * width + (x + dx)])
                        
                        if len(block) > 1:
                            variance = statistics.variance(block)
                            if variance > 1000:  # High variance indicates irregular texture
                                high_variance_blocks += 1
                            total_blocks += 1
                
                if total_blocks > 0:
                    irregular_ratio = high_variance_blocks / total_blocks
                    if irregular_ratio > 0.3:
                        score += 15
            
            return score
            
        except Exception as e:
            logger.error(f"Error in texture analysis: {str(e)}")
            return 0
    
    def calculate_edge_density(self, gray_image):
        """
        Calculate edge density using simple gradient approximation
        Returns edge density ratio
        """
        try:
            width, height = gray_image.size
            pixels = list(gray_image.getdata())
            
            edge_count = 0
            total_pixels = 0
            
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    center = pixels[y * width + x]
                    
                    # Check horizontal and vertical gradients
                    left = pixels[y * width + (x - 1)]
                    right = pixels[y * width + (x + 1)]
                    top = pixels[(y - 1) * width + x]
                    bottom = pixels[(y + 1) * width + x]
                    
                    h_gradient = abs(right - left)
                    v_gradient = abs(bottom - top)
                    
                    if h_gradient > 50 or v_gradient > 50:
                        edge_count += 1
                    
                    total_pixels += 1
            
            return edge_count / total_pixels if total_pixels > 0 else 0
            
        except Exception as e:
            logger.error(f"Error calculating edge density: {str(e)}")
            return 0
    
    def determine_hazard_type(self, image_path, visual_score, color_score, texture_score):
        """
        Determine the most likely hazard type based on analysis scores
        Returns hazard type string
        """
        try:
            filename = os.path.basename(image_path).lower()
            
            # Check filename for specific hazard types
            if any(term in filename for term in ['road', 'pothole', 'street', 'pavement']):
                return 'road'
            elif any(term in filename for term in ['building', 'bridge', 'construction', 'infrastructure']):
                return 'infrastructure'
            elif any(term in filename for term in ['fire', 'flood', 'tree', 'environment']):
                return 'environment'
            elif any(term in filename for term in ['garbage', 'waste', 'sewage', 'pollution']):
                return 'health'
            elif any(term in filename for term in ['danger', 'unsafe', 'accident', 'safety']):
                return 'public'
            
            # If no filename clues, use visual analysis
            if visual_score > 15 and texture_score > 10:
                return 'road'  # Likely road damage
            elif color_score > 15:
                return 'environment'  # Likely environmental issue
            else:
                return 'other'
                
        except Exception as e:
            logger.error(f"Error determining hazard type: {str(e)}")
            return 'other'

# Global classifier instance
hazard_classifier = None

def get_hazard_classifier():
    """Get or create the global hazard classifier instance"""
    global hazard_classifier
    if hazard_classifier is None:
        hazard_classifier = HazardImageClassifier()
    return hazard_classifier

def validate_hazard_image(image_path):
    """
    Validate if an image is hazard-related
    Returns: (is_valid: bool, confidence: float, hazard_type: str, message: str)
    """
    try:
        classifier = get_hazard_classifier()
        is_hazard, confidence, hazard_type, reason = classifier.is_hazard_related(image_path)
        
        if is_hazard:
            message = f"Valid hazard image detected ({confidence:.1f}% confidence)"
        else:
            message = "Please upload a related picture."
        
        return is_hazard, confidence, hazard_type, message
        
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        # In case of error, allow the upload but log the error
        return True, 50.0, "unknown", "Image validation completed"