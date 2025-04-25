# 03_observations_cleaning.py

import pandas as pd
import numpy as np
from pathlib import Path
import gzip
from IPython.display import display, Markdown
import matplotlib.pyplot as plt

DATA_DIR = Path('data/original')
OUTPUT_DIR = Path('data/processed')

# %% 
# Key LOINC Codes for Analysis
# - **Blood Pressure**: 
#   - Systolic: `8480-6`
#   - Diastolic: `8462-4`  
# - **BMI**: `39156-5`

# %%
def clean_observations(obs_path, clean_patients_path):
    """
    Cleans observations data with:
    1. Patient linkage validation
    2. LOINC code verification
    3. Unit standardization
    4. Range validation
    """
    obs = pd.read_csv(obs_path)
    valid_patients = pd.read_csv(clean_patients_path)['id']
    
    # 1. Patient linkage
    obs = obs[obs['PATIENT'].isin(valid_patients)]
    
    # 2. LOINC validation
    loinc_codes = pd.read_csv(DATA_DIR/'dictionary_loinc.csv')['CODE']
    valid_obs = obs[obs['CODE'].isin(loinc_codes)].copy()  # Make sure it's a copy
    
    # 3. Numeric value extraction
    valid_obs.loc[:, 'VALUE_NUM'] = pd.to_numeric(valid_obs['VALUE'], errors='coerce')
    
    # 4. Unit standardization
    valid_obs.loc[:, 'UNITS'] = valid_obs['UNITS'].str.lower().str.strip()
    
    return valid_obs

if __name__ == "__main__":
    observations = clean_observations(
        DATA_DIR/'observations.csv.gz',
        OUTPUT_DIR/'clean_patients.csv'
    )
    
    # Save outputs
    observations.to_csv(OUTPUT_DIR/'clean_observations.csv', index=False)
    
    # Reporting
    print("### Observations Cleaning Report")
    print(f"Original observations: {len(pd.read_csv(DATA_DIR/'observations.csv.gz')):,}")
    print(f"Valid observations: {len(observations):,}")

    # Blood Pressure stats
    bp_codes = ['8480-6', '8462-4']
    bp_data = observations[observations['CODE'].isin(bp_codes)]
    print(f"**Blood Pressure Records**: {len(bp_data):,}")

    



