import pandas as pd
import os
from pathlib import Path
import io
import re

class ForkliftData:
    """
    Class to load and access forklift data from CSV files and brochures
    """
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.specs_df = None
        self.rates_df = None
        self.brochure_content = {}
        self._load_data()
    
    def _load_data(self):
        """Load all data sources"""
        self._load_specs()
        self._load_rates()
        self._load_brochures()
    
    def _load_specs(self):
        """Load forklift specifications"""
        # For this example, we'll extract specs from the brochure PDFs
        # In a real application, you would parse the PDFs or use a dedicated specs CSV
        specs_data = []
        
        # Extract specs from the brochure data we have
        # D35-40-45-50-55 series
        specs_data.extend([
            {"model": "D35s-5", "capacity_kg": 3500, "capacity_tons": 3.5, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D40s-5", "capacity_kg": 4000, "capacity_tons": 4.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D45s-5", "capacity_kg": 4500, "capacity_tons": 4.5, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D50C-5", "capacity_kg": 5000, "capacity_tons": 5.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D55C-5", "capacity_kg": 5500, "capacity_tons": 5.5, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
        ])
        
        # D60-70-80-90 series
        specs_data.extend([
            {"model": "D60s-5", "capacity_kg": 6000, "capacity_tons": 6.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D70s-5", "capacity_kg": 7000, "capacity_tons": 7.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D80s-5", "capacity_kg": 8000, "capacity_tons": 8.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
            {"model": "D90s-5", "capacity_kg": 9000, "capacity_tons": 9.0, "load_center_mm": 600, "fuel_type": "Diesel", "series": "5-Series"},
        ])
        
        # Create DataFrame from extracted specs
        self.specs_df = pd.DataFrame(specs_data)
    
    def _load_rates(self):
        """Load rental rates"""
        try:
            # Read rates from CSV
            rates_path = self.data_dir / "Schedule of Rates Example - Sheet1.csv"
            self.rates_df = pd.read_csv(rates_path)
            
            # Clean the data
            self.rates_df.columns = self.rates_df.columns.str.strip()
            
            # Extract and clean rate columns
            for col in self.rates_df.columns[1:]:  # Skip the first column (Equipment Description)
                if self.rates_df[col].dtype == object:
                    # Remove $ and commas, convert to float
                    self.rates_df[col] = self.rates_df[col].str.replace('$', '', regex=False)
                    self.rates_df[col] = self.rates_df[col].str.replace(',', '', regex=False)
                    self.rates_df[col] = self.rates_df[col].str.strip()
                    self.rates_df[col] = pd.to_numeric(self.rates_df[col], errors='coerce')
        except Exception as e:
            print(f"Error loading rates: {e}")
            # Create a fallback rates dataframe
            self.rates_df = pd.DataFrame({
                "Equipment Description": [
                    "Diesel 2.5t Forklift", "Diesel 3t Forklift", "Diesel 4t Forklift", 
                    "Diesel 5t Forklift", "Diesel 7t Forklift"
                ],
                "Daily Rate (Inc GST) 0-7 Days": [44.00, 55.00, 30.00, 35.00, 35.00],
                "Weekly Rate (Inc GST) 8-28 Days": [245.00, 336.00, 140.00, 175.00, 175.00],
                "Weekly Rate (Inc GST) 28+ Days": [140.00, 210.00, 105.00, 126.00, 126.00]
            })
    
    def _load_brochures(self):
        """Load brochure content"""
        # In a real app, you would extract text from PDF files
        # Here we're simulating with the content we have
        
        # D35-40-45-50-55 series brochure
        self.brochure_content["D35-D55"] = """
        Diesel forklifts 5-Series, Pneumatic, 3.5 to 5.5 ton capacity
        
        FEATURES:
        - Safety first: Protect your investment, workforce, and handled goods with excellent all-around visibility, reliable oil-cooled brakes, and many standard safety features.
        - Powerful and efficient: High-performance engines with 2-speed power shift transmission and up to 67.7kW of power.
        - Built tough: Robust mast design, engine shutdown, and anti-dust frame & component.
        - Comfortable all shift long: Spacious cab with plenty of legroom, deluxe suspended seat, integrated instrument panel, and tiltable steering column.
        
        SAFETY FEATURES:
        - Operator Sensing System (OSS)
        - Excellent visibility through the mast
        - Oil-cooled Disc Brakes
        - Mast lowering interlock & tilt lock
        - Parking brake alert
        - Rear view mirror and backup alarm
        
        SPECIFICATIONS:
        - Load capacity: 3,500 to 5,500 kg
        - Load center: 600 mm
        - Lift height: up to 6,050 mm
        - Powerful diesel engines
        - Oil-cooled disc brakes
        """
        
        # D60-70-80-90 series brochure
        self.brochure_content["D60-D90"] = """
        Diesel forklifts 5-Series, Pneumatic, 6.0 to 9.0 ton capacity
        
        FEATURES:
        - Safety first: Protect your investment, workforce, and handled goods with excellent all-around visibility, reliable brakes, and many standard safety features.
        - Powerful and efficient: High-performance engines with 2-speed or 3-speed transmission and up to 73.5kW of power.
        - Built tough: Superior hydrostatic steering system designed for high shock absorption, rugged frame, fully floating drive axle, and oil-cooled brakes.
        - Comfortable all shift long: Spacious cab with plenty of legroom, suspension seat, integrated instrument panel, and tiltable steering column.
        
        SAFETY FEATURES:
        - Operator Sensing System (OSS)
        - Excellent visibility through the mast
        - Oil-cooled Disc Brakes
        - Mast lowering interlock & tilt lock
        - Parking brake alert
        - Rear view mirror and backup alarm
        - Weight scale to prevent overloading
        
        SPECIFICATIONS:
        - Load capacity: 6,000 to 9,000 kg
        - Load center: 600 mm
        - Lift height: up to 6,000 mm
        - Powerful diesel engines
        - Oil-cooled disc brakes
        """
    
    def get_forklift_by_capacity(self, capacity_tons):
        """Find a forklift model based on capacity requirements"""
        # Convert to numeric if it's a string
        if isinstance(capacity_tons, str):
            capacity_tons = float(re.findall(r'\d+\.?\d*', capacity_tons)[0])
        
        # Find models that meet or exceed the capacity requirement
        valid_models = self.specs_df[self.specs_df['capacity_tons'] >= capacity_tons]
        
        if valid_models.empty:
            return None
        
        # Return the smallest suitable forklift (most efficient option)
        return valid_models.sort_values('capacity_tons').iloc[0]
    
    def get_rate_for_model(self, model, rental_days):
        """Get the rental rate for a particular model and duration"""
        # Match model to equipment description
        capacity_tons = self.specs_df.loc[self.specs_df['model'] == model, 'capacity_tons'].iloc[0]
        equipment_desc = f"Diesel {capacity_tons}t Forklift"
        
        # Find the closest match in rates DataFrame
        closest_match = None
        
        for _, row in self.rates_df.iterrows():
            desc = row['Equipment Description']
            if 'Diesel' in desc and 'Forklift' in desc:
                try:
                    # Extract tonnage from the description
                    tonnage = float(re.findall(r'(\d+\.?\d*)t', desc)[0])
                    if closest_match is None or abs(tonnage - capacity_tons) < abs(closest_match[0] - capacity_tons):
                        closest_match = (tonnage, row)
                except (IndexError, ValueError):
                    continue
        
        if closest_match is None:
            return {
                "daily": 50.0,   # Default rates if no match found
                "weekly_short": 280.0,
                "weekly_long": 200.0
            }
        
        # Determine which rate to apply based on rental duration
        rate_row = closest_match[1]
        if rental_days <= 7:
            rate = rate_row['Daily Rate (Inc GST) 0-7 Days']
        elif rental_days <= 28:
            rate = rate_row['Weekly Rate (Inc GST) 8-28 Days'] / 7  # Convert weekly to daily
        else:
            rate = rate_row['Weekly Rate (Inc GST) 28+ Days'] / 7  # Convert weekly to daily
        
        return {
            "daily": float(rate_row['Daily Rate (Inc GST) 0-7 Days']),
            "weekly_short": float(rate_row['Weekly Rate (Inc GST) 8-28 Days']),
            "weekly_long": float(rate_row['Weekly Rate (Inc GST) 28+ Days']),
            "applied_rate": float(rate),
            "total_cost": float(rate * rental_days)
        }
    
    def get_brochure_content(self, model):
        """Get brochure content for a specific model"""
        if "D35" <= model <= "D55":
            return self.brochure_content["D35-D55"]
        elif "D60" <= model <= "D90":
            return self.brochure_content["D60-D90"]
        else:
            return "Brochure not available for this model."
