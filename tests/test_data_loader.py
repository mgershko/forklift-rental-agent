import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to the path to import the application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import ForkliftData

class TestDataLoader(unittest.TestCase):
    """Test cases for the ForkliftData class"""
    
    def setUp(self):
        """Set up the test environment"""
        self.data = ForkliftData()
    
    def test_specs_loaded(self):
        """Test that specifications are loaded correctly"""
        self.assertIsNotNone(self.data.specs_df, "Specs dataframe should not be None")
        self.assertGreater(len(self.data.specs_df), 0, "Specs dataframe should have at least one row")
        
        # Check that required columns exist
        required_columns = ['model', 'capacity_kg', 'capacity_tons', 'fuel_type']
        for col in required_columns:
            self.assertIn(col, self.data.specs_df.columns, f"Column '{col}' should exist in specs dataframe")
    
    def test_rates_loaded(self):
        """Test that rates are loaded correctly"""
        self.assertIsNotNone(self.data.rates_df, "Rates dataframe should not be None")
        self.assertGreater(len(self.data.rates_df), 0, "Rates dataframe should have at least one row")
        
        # Check that required columns exist
        required_columns = [
            'Equipment Description', 
            'Daily Rate (Inc GST) 0-7 Days',
            'Weekly Rate (Inc GST) 8-28 Days',
            'Weekly Rate (Inc GST) 28+ Days'
        ]
        for col in required_columns:
            self.assertIn(col, self.data.rates_df.columns, f"Column '{col}' should exist in rates dataframe")
    
    def test_brochures_loaded(self):
        """Test that brochure content is loaded correctly"""
        self.assertIsNotNone(self.data.brochure_content, "Brochure content should not be None")
        self.assertGreater(len(self.data.brochure_content), 0, "Brochure content should have at least one entry")
        
        # Check that brochure content for both series exists
        self.assertIn("D35-D55", self.data.brochure_content, "D35-D55 series brochure should exist")
        self.assertIn("D60-D90", self.data.brochure_content, "D60-D90 series brochure should exist")
    
    def test_get_forklift_by_capacity(self):
        """Test that the right forklift is returned based on capacity"""
        # Test with a numeric capacity
        forklift_3_5t = self.data.get_forklift_by_capacity(3.5)
        self.assertIsNotNone(forklift_3_5t, "Should find a forklift for 3.5 ton capacity")
        self.assertEqual(forklift_3_5t['model'], "D35s-5", "Should return D35s-5 for 3.5 ton capacity")
        
        # Test with a string capacity
        forklift_4t = self.data.get_forklift_by_capacity("4 tons")
        self.assertIsNotNone(forklift_4t, "Should find a forklift for '4 tons' capacity")
        self.assertEqual(forklift_4t['model'], "D40s-5", "Should return D40s-5 for 4 ton capacity")
        
        # Test with a capacity in kg
        forklift_5000kg = self.data.get_forklift_by_capacity("5000 kg")
        self.assertIsNotNone(forklift_5000kg, "Should find a forklift for '5000 kg' capacity")
        self.assertEqual(forklift_5000kg['model'], "D50C-5", "Should return D50C-5 for 5000 kg capacity")
        
        # Test with a capacity that's too high for any model
        forklift_too_heavy = self.data.get_forklift_by_capacity(10.0)
        self.assertIsNone(forklift_too_heavy, "Should return None for capacity that's too high")
    
    def test_get_rate_for_model(self):
        """Test that the correct rate is returned for a model and duration"""
        # Test for a short-term rental (<=7 days)
        model = "D35s-5"
        rental_days = 5
        rate_info = self.data.get_rate_for_model(model, rental_days)
        
        self.assertIsNotNone(rate_info, "Rate information should not be None")
        self.assertIn('daily', rate_info, "Rate info should include daily rate")
        self.assertIn('weekly_short', rate_info, "Rate info should include short-term weekly rate")
        self.assertIn('weekly_long', rate_info, "Rate info should include long-term weekly rate")
        self.assertIn('applied_rate', rate_info, "Rate info should include the applied rate")
        self.assertIn('total_cost', rate_info, "Rate info should include the total cost")
        
        # Test that total cost is calculated correctly
        self.assertAlmostEqual(
            rate_info['total_cost'], 
            rate_info['applied_rate'] * rental_days, 
            places=2, 
            msg="Total cost should be daily rate * rental days"
        )
        
        # Test for a long-term rental (>28 days)
        rental_days = 30
        rate_info_long = self.data.get_rate_for_model(model, rental_days)
        self.assertLess(
            rate_info_long['applied_rate'], 
            rate_info['applied_rate'], 
            "Long-term rate should be lower than short-term rate"
        )
    
    def test_get_brochure_content(self):
        """Test that the correct brochure content is returned for a model"""
        # Test for a model in the D35-D55 series
        model = "D35s-5"
        brochure = self.data.get_brochure_content(model)
        self.assertIsNotNone(brochure, "Brochure content should not be None")
        self.assertIn("3.5 to 5.5 ton capacity", brochure, "Brochure should mention the capacity range")
        
        # Test for a model in the D60-D90 series
        model = "D60s-5"
        brochure = self.data.get_brochure_content(model)
        self.assertIsNotNone(brochure, "Brochure content should not be None")
        self.assertIn("6.0 to 9.0 ton capacity", brochure, "Brochure should mention the capacity range")
        
        # Test for a non-existent model
        model = "X999"
        brochure = self.data.get_brochure_content(model)
        self.assertIn("not available", brochure.lower(), "Brochure should indicate it's not available")

if __name__ == '__main__':
    unittest.main()
