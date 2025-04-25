# 04_medications_cleaning.py

import pandas as pd
import numpy as np
from pathlib import Path
from IPython.display import display, Markdown
import gzip

# Configuration
DATA_DIR = Path('data/original')
OUTPUT_DIR = Path('data/processed')

def load_medications(meds_path, clean_patients_path):
    # Load raw medications
    medications = pd.read_csv(meds_path)
    valid_patients = pd.read_csv(clean_patients_path)['id']

    # Filter to valid patients
    medications = medications[medications['PATIENT'].isin(valid_patients)]

    # Normalize CODE field for matching
    medications['CODE'] = pd.to_numeric(medications['CODE'], errors='coerce').dropna().astype(int).astype(str)

    # Load and normalize RXNORM dictionary
    rxnorm_codes = pd.read_csv(DATA_DIR / 'dictionary_rxnorm.csv')
    rxnorm_codes['CODE'] = rxnorm_codes['CODE'].astype(str)

    # Filter meds by valid RXNORM codes
    valid_meds = medications[medications['CODE'].isin(rxnorm_codes['CODE'])]

    return medications, valid_meds, rxnorm_codes

if __name__ == "__main__":
    raw_meds, valid_meds, rxnorm = load_medications(
        DATA_DIR / 'medications.csv.gz',
        OUTPUT_DIR / 'clean_patients.csv'
    )

    # Save cleaned output
    valid_meds.to_csv(OUTPUT_DIR / 'clean_medications.csv', index=False)

    # Reporting
    display(Markdown("### Medications Cleaning Report"))
    print(f"Total raw medications: {len(raw_meds)}")
    print(f"Valid medications: {len(valid_meds)}")
    print(f"Unique patients in meds: {raw_meds['PATIENT'].nunique()}")
    print(f"Overlap with clean patients: {raw_meds['PATIENT'].isin(pd.read_csv(OUTPUT_DIR / 'clean_patients.csv')['id']).sum()}")
    print(f"Unique RXNORM codes in meds: {raw_meds['CODE'].nunique()}")
    print(f"Overlap with RXNORM dict: {valid_meds['CODE'].nunique()}")

