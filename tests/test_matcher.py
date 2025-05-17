import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to the path to import the application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.matcher import ForkliftMatcher
from src.data_loader import ForkliftData

class TestMatcher(unittest.TestCase):
    """Test cases for the ForkliftMatcher class"""
    
    def setUp(self):
        """Set up the test environment"""
        self.data = ForkliftData()
        self.matcher = ForkliftMatcher(self.data)
    
    def test_normalize_weight(self):
        """Test that weight is normalized correctly"""
        # Test with numeric values
        self.assertEqual(self.matcher._normalize_weight(3.5), 3.5, "Should return the same value for numeric input")
        self.assertEqual(self.matcher._normalize_weight(4), 4.0, "Should convert integers to floats")
        
        # Test with string values
        self.assertEqual(self.matcher._normalize_weight("2 tons"), 2.0, "Should extract numeric value from string with 'tons'")
        self.assertEqual(self.matcher._normalize_weight("2000 kg"), 2.0, "Should convert kg to tons")
        self.assertEqual(self.matcher._normalize_weight("3500kg"), 3.5, "Should handle no space between number and unit")
        
        # Test with invalid input
        self.assertEqual(self.matcher._normalize_weight("invalid"), 0.0, "Should return 0.0 for invalid input")
    
    def test_match_forklift(self):
        """Test that the right forklift is matched based on requirements"""
        # Test with basic requirements
        requirements = {
            'load_weight': '3 tons',
            'rental_period': 7,
            'indoor_outdoor': 'outdoor'
        }
        
        match_result = self.matcher.match_forklift(requirements)
        
        # Check that the match was successful
        self.assertTrue(match_result['success'], "Match should be successful")
        
        # Check that the returned forklift has sufficient capacity (with safety margin)
        # 3 tons with 20% safety margin = 3.6 tons, so should return a 4-ton forklift (D40s-5)
        self.assertEqual(match_result['forklift']['model'], "D40s-5", "Should return D40s-5 for 3 ton requirement")
        
        # Test with higher weight requirement
        requirements = {
            'load_weight': '6 tons',
            'rental_period': 14,
            'indoor_outdoor': 'both'
        }
        
        match_result = self.matcher.match_forklift(requirements)
        
        # Check that the match was successful
        self.assertTrue(match_result['success'], "Match should be successful")
        
        # 6 tons with 20% safety margin = 7.2 tons, so should return an 8-ton forklift (D80s-5)
        self.assertEqual(match_result['forklift']['model'], "D80s-5", "Should return D80s-5 for 6 ton requirement")
        
        # Test with too high weight requirement
        requirements = {
            'load_weight': '10 tons',
            'rental_period': 7,
            'indoor_outdoor': 'outdoor'
        }
        
        match_result = self.matcher.match_forklift(requirements)
        
        # Check that the match was unsuccessful
        self.assertFalse(match_result['success'], "Match should be unsuccessful for too high capacity")
        self.assertIn("No suitable forklift found", match_result['message'], "Should return appropriate error message")
    
    def test_usage_recommendation(self):
        """Test that appropriate usage recommendations are provided"""
        # Get a forklift to test with
        forklift = self.data.get_forklift_by_capacity(4.0)
        
        # Test recommendation for indoor use
        indoor_rec = self.matcher._get_usage_recommendation(forklift, 'indoor')
        self.assertIn("ventilation", indoor_rec, "Indoor recommendation should mention ventilation")
        self.assertIn("LPG", indoor_rec, "Indoor recommendation should mention LPG alternatives")
        
        # Test recommendation for outdoor use
        outdoor_rec = self.matcher._get_usage_recommendation(forklift, 'outdoor')
        self.assertIn("well-suited", outdoor_rec, "Outdoor recommendation should mention forklift is well-suited")
        self.assertIn("traction", outdoor_rec, "Outdoor recommendation should mention traction")
        
        # Test recommendation for mixed use
        mixed_rec = self.matcher._get_usage_recommendation(forklift, 'both')
        self.assertIn("ventilated", mixed_rec, "Mixed recommendation should mention ventilation")
        self.assertIn("LPG", mixed_rec, "Mixed recommendation should mention LPG alternatives")
    
    def test_safety_info(self):
        """Test that safety information is provided"""
        # Get a forklift to test with
        forklift = self.data.get_forklift_by_capacity(4.0)
        
        safety_info = self.matcher._get_safety_info(forklift)
        self.assertIn("Operator Sensing System", safety_info, "Safety info should mention OSS")
        self.assertIn("certified", safety_info, "Safety info should mention certification requirements")
        self.assertIn("safety checks", safety_info, "Safety info should mention safety checks")

if __name__ == '__main__':
    unittest.main()
