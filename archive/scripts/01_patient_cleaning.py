# 01_patient_cleaning.py

import pandas as pd
import numpy as np
import gzip
from pathlib import Path

# Configuration
data_dir = Path('data/original')
output_dir = Path('data/processed')
output_dir.mkdir(exist_ok=True)
VALID_AGE_RANGE = (0, 120)

def load_gzipped_csv(path):
    with gzip.open(path, 'rb') as f:
        return pd.read_csv(f)

def clean_patients_data(patients):
    patients.columns = patients.columns.str.lower()
    
    # Date handling
    patients['birthdate'] = pd.to_datetime(patients['birthdate'], errors='coerce')
    patients['age'] = (pd.to_datetime('today') - patients['birthdate']).dt.days / 365.25
    
    # Age validation
    patients['age'] = np.where(
        (patients['age'] < VALID_AGE_RANGE[0]) | (patients['age'] > VALID_AGE_RANGE[1]),
        np.nan,
        patients['age']
    )
    
    # Demographics cleaning
    patients['gender'] = patients['gender'].map({'M': 'M', 'F': 'F', '8293.3': np.nan})
    
    # Simplified race cleaning (since data is already clean)
    patients['race'] = patients['race'].str.lower()
    valid_races = ['white', 'black', 'asian', 'hawaiian', 'other', 'native']
    patients['race'] = patients['race'].where(
        patients['race'].isin(valid_races),  # Keep if valid
        'other'  # Replace invalid values
    )
    
    # Quality flags
    patients['data_quality_flag'] = np.where(
        patients[['birthdate', 'gender', 'age']].isna().any(axis=1),
        'Invalid',
        'Valid'
    )
    
    return patients

def print_race_verification(patients, clean_patients):
    print("\n=== Race Distribution Verification ===")
    
    # Get all unique original race values
    print("\nAll original race values:")
    print(np.sort(patients['race'].unique()))
    
    # Show cleaned distribution
    print("\nCleaned race categories with counts:")
    print(clean_patients['race'].value_counts())
    
    # Detailed breakdown
    print("\nOriginal -> Cleaned mapping examples:")
    for category in clean_patients['race'].unique():
        original_values = patients.loc[patients['race'].str.lower() == category.lower(), 'race'].unique()
        print(f"\n{category} (n={len(clean_patients[clean_patients['race'] == category])}):")
        print(f"Original values: {original_values[:5]}")  # Show first 5 examples
        if category == 'other':
            non_standard = patients[~patients['race'].str.lower().isin(
                ['white','black','asian','hawaiian','native'])]['race'].unique()
            print(f"Non-standard values mapped to 'other': {non_standard}")

if __name__ == "__main__":
    # Load and clean
    patients = load_gzipped_csv(data_dir / 'patients.csv.gz')
    clean_patients = clean_patients_data(patients)
    
    # Split and save
    valid_patients = clean_patients[clean_patients['data_quality_flag'] == 'Valid']
    invalid_patients = clean_patients[clean_patients['data_quality_flag'] == 'Invalid']
    
    valid_patients.to_csv(output_dir / 'clean_patients.csv', index=False)
    invalid_patients.to_csv(output_dir / 'excluded_patients.csv', index=False)
    
    # Reporting
    print("\n=== Final Cleaning Report ===")
    print(f"Initial patients: {len(patients)}")
    print(f"Valid patients: {len(valid_patients)} ({len(valid_patients)/len(patients):.1%})")
    print(f"Excluded patients: {len(invalid_patients)}")
    
    print("\nFinal age distribution (years):")
    print(valid_patients['age'].describe())
    
    # Race verification
    print_race_verification(patients, valid_patients)   
