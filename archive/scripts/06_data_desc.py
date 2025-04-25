# 06_data_desc.py

import pandas as pd
from pathlib import Path  # Make sure to import Path

# Paths to cleaned data
OUTPUT_DIR = Path('data/processed')
clean_patients = pd.read_csv(OUTPUT_DIR / 'clean_patients.csv')
clean_conditions = pd.read_csv(OUTPUT_DIR / 'clean_conditions.csv')
clean_observations = pd.read_csv(OUTPUT_DIR / 'clean_observations.csv')
clean_medications = pd.read_csv(OUTPUT_DIR / 'clean_medications.csv')
clean_encounters = pd.read_csv(OUTPUT_DIR / 'clean_encounters.csv')

# 1. Unique patients in each dataset
print(f"Unique patients in clean_patients: {clean_patients['id'].nunique()}")
print(f"Unique patients in clean_conditions: {clean_conditions['PATIENT'].nunique()}")
print(f"Unique patients in clean_observations: {clean_observations['PATIENT'].nunique()}")
print(f"Unique patients in clean_medications: {clean_medications['PATIENT'].nunique()}")
print(f"Unique patients in clean_encounters: {clean_encounters['PATIENT'].nunique()}")

# 2. Most frequent ontology terms (SNOMED, LOINC, RXNORM)
# Conditions: SNOMED codes
print("\nMost frequent SNOMED codes in conditions:")
print(clean_conditions['CODE'].value_counts().head())

# Observations: LOINC codes
print("\nMost frequent LOINC codes in observations:")
print(clean_observations['CODE'].value_counts().head())

# Medications: RXNORM codes
print("\nMost frequent RXNORM codes in medications:")
print(clean_medications['CODE'].value_counts().head())

# 3. General stats (optional, you can expand with other metrics)
print("\nGeneral stats for cleaned data:")

# Clean patients
print(f"\nClean patients data summary:\n{clean_patients.describe()}")

# Clean conditions
print(f"\nClean conditions data summary:\n{clean_conditions.describe()}")

# Clean observations
print(f"\nClean observations data summary:\n{clean_observations.describe()}")

# Clean medications
print(f"\nClean medications data summary:\n{clean_medications.describe()}")

# Clean encounters
print(f"\nClean encounters data summary:\n{clean_encounters.describe()}")

