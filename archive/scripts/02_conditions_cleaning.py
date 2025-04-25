# 02_conditions_cleaning.py

import pandas as pd
import numpy as np
from pathlib import Path
import gzip
from IPython.display import display, Markdown

DATA_DIR = Path('data/original')
OUTPUT_DIR = Path('data/processed')

def load_conditions(conditions_path, clean_patients_path):
    """Load and validate conditions data"""
    conditions = pd.read_csv(conditions_path)
    valid_patients = pd.read_csv(clean_patients_path)['id']
    
    # QC Checks
    conditions = conditions[conditions['PATIENT'].isin(valid_patients)]
    conditions['START'] = pd.to_datetime(conditions['START'], errors='coerce')
    
    # SNOMED Validation
    snomed_codes = pd.read_csv(DATA_DIR/'dictionary_snomed.csv')['CODE']
    valid_conditions = conditions[conditions['CODE'].isin(snomed_codes)]
    
    return valid_conditions


if __name__ == "__main__":
    conditions = load_conditions(
        DATA_DIR/'conditions.csv.gz',
        OUTPUT_DIR/'clean_patients.csv'
    )
    
    # Save results
    conditions.to_csv(OUTPUT_DIR/'clean_conditions.csv', index=False)
    
    # Reporting
    display(Markdown("### Conditions Cleaning Report"))
    display(f"Initial conditions: {len(pd.read_csv(DATA_DIR/'conditions.csv.gz'))}")
    display(f"Valid conditions: {len(conditions)}")
    display(f"SNOMED codes: {conditions['CODE'].nunique()} unique codes")
