# 05_encounters_cleaning.py

import pandas as pd
import numpy as np
from pathlib import Path
import gzip

# Configuration
DATA_DIR = Path('data/original')
OUTPUT_DIR = Path('data/processed')

def load_encounters(encounters_path, clean_patients_path):
    """Load and validate encounters data"""
    encounters = pd.read_csv(encounters_path)
    valid_patients = pd.read_csv(clean_patients_path)['id']
    
    # QC: Filter encounters with valid patient IDs
    encounters = encounters[encounters['PATIENT'].isin(valid_patients)]
    
    # Handle date columns: Convert to datetime, coerce errors
    encounters['START'] = pd.to_datetime(encounters['START'], errors='coerce')
    encounters['STOP'] = pd.to_datetime(encounters['STOP'], errors='coerce')
    
    # Filter out any rows with invalid dates or missing key fields
    encounters = encounters.dropna(subset=['PATIENT', 'START'])
    
    # Add any additional cleaning logic based on specific encounter attributes
    return encounters

if __name__ == "__main__":
    encounters = load_encounters(
        DATA_DIR/'encounters.csv.gz',
        OUTPUT_DIR/'clean_patients.csv'
    )
    
    # Save cleaned encounters data
    encounters.to_csv(OUTPUT_DIR/'clean_encounters.csv', index=False)
    
    # Reporting
    print(f"Initial encounters: {len(pd.read_csv(DATA_DIR/'encounters.csv.gz'))}")
    print(f"Valid encounters: {len(encounters)}")
    print(f"Unique patients in encounters: {encounters['PATIENT'].nunique()}")

