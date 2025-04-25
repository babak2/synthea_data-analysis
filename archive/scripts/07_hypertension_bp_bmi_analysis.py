# 07_hypertension_bp_bmi_analysis.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load Data ---
print("Loading data...")
conditions = pd.read_csv("data/original/conditions.csv.gz")
observations = pd.read_csv("data/original/observations.csv.gz")

# --- Identify hypertensive patients ---
print("Identifying hypertensive patients...")
hypertension_code = 59621000
hypertension_patients = conditions[conditions['CODE'] == hypertension_code]['PATIENT'].unique()
print(f"Number of hypertensive patients: {len(hypertension_patients)}")

# --- Filter BP observations ---
print("Filtering BP observations...")
bp_codes = ['8462-4', '8480-6']  # Diastolic, Systolic
observations['VALUE'] = pd.to_numeric(observations['VALUE'], errors='coerce')
bp_obs = observations[observations['CODE'].isin(bp_codes)]
bp_obs_hyper = bp_obs[bp_obs['PATIENT'].isin(hypertension_patients)].copy()

# Pivot systolic/diastolic per patient-date-encounter
bp_pivot = bp_obs_hyper.pivot_table(
    index=['DATE', 'PATIENT', 'ENCOUNTER'],
    columns='CODE',
    values='VALUE'
).reset_index().rename(columns={'8480-6': 'SYSTOLIC_BP', '8462-4': 'DIASTOLIC_BP'})
print(f"Blood pressure observations: {len(bp_pivot)}")

# --- Filter BMI observations ---
print("Filtering BMI observations...")
bmi_code = '39156-5'
bmi_obs = observations[(observations['CODE'] == bmi_code) & (observations['PATIENT'].isin(hypertension_patients))]
bmi_obs['VALUE'] = pd.to_numeric(bmi_obs['VALUE'], errors='coerce')
print(f"BMI observations: {len(bmi_obs)}")

# --- Summary ---
print("\n--- Summary Statistics ---")
print(bp_pivot[['SYSTOLIC_BP', 'DIASTOLIC_BP']].describe())
print("\nBMI Summary:")
print(bmi_obs['VALUE'].describe())

# --- Plots ---
plt.figure(figsize=(12, 5))
sns.kdeplot(bp_pivot['SYSTOLIC_BP'].dropna(), label="Systolic", fill=True)
sns.kdeplot(bp_pivot['DIASTOLIC_BP'].dropna(), label="Diastolic", fill=True)
plt.title("Distribution of Blood Pressure (Hypertensive Patients)")
plt.xlabel("Blood Pressure (mmHg)")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.kdeplot(bmi_obs['VALUE'].dropna(), label="BMI", fill=True, color="purple")
plt.title("Distribution of BMI (Hypertensive Patients)")
plt.xlabel("BMI")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

