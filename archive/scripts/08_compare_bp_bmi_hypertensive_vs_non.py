# 08_compare_bp_bmi_hypertensive_vs_non.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


# Configuration
DATA_DIR = Path("data/original")
OUTPUT_DIR = Path("data/processed")

# Load data
print("Loading data...")
conditions = pd.read_csv(DATA_DIR / "conditions.csv.gz", compression="gzip")
observations = pd.read_csv(DATA_DIR / "observations.csv.gz", compression="gzip")

# Show a sample of the conditions DataFrame
print("\n--- Sample of Conditions DataFrame ---")
print(conditions.head())

# Ensure 'CODE' is string for comparison
conditions["CODE"] = conditions["CODE"].astype(str).str.strip()

# Hypertension SNOMED codes
hypertensive_codes = ["10509002.0", "283371005.0", "444814009.0"]

# Identify hypertensive patients
print("\nIdentifying hypertensive patients...")
hypertensive_patients = conditions[conditions["CODE"].isin(hypertensive_codes)]["PATIENT"].unique()
print(f"Number of hypertensive patients: {len(hypertensive_patients)}")

# Filter for Systolic, Diastolic BP, and BMI
systolic_code = "8480-6"
diastolic_code = "8462-4"
bmi_code = "39156-5"

# Make sure 'CODE' is string in observations too
observations["CODE"] = observations["CODE"].astype(str).str.strip()

# Extract relevant observations
bp_sys = observations[observations["CODE"] == systolic_code][["PATIENT", "VALUE"]].rename(columns={"VALUE": "SYSTOLIC_BP"})
bp_dia = observations[observations["CODE"] == diastolic_code][["PATIENT", "VALUE"]].rename(columns={"VALUE": "DIASTOLIC_BP"})
bmi = observations[observations["CODE"] == bmi_code][["PATIENT", "VALUE"]].rename(columns={"VALUE": "BMI"})

# Merge BP readings
bp = pd.merge(bp_sys, bp_dia, on="PATIENT", how="inner")

# Merge with BMI
bp_bmi = pd.merge(bp, bmi, on="PATIENT", how="inner")

# Tag hypertensive vs non-hypertensive
bp_bmi["HYPERTENSIVE"] = bp_bmi["PATIENT"].isin(hypertensive_patients)

# Convert columns to numeric, forcing errors to NaN
bp_bmi["SYSTOLIC_BP"] = pd.to_numeric(bp_bmi["SYSTOLIC_BP"], errors='coerce')
bp_bmi["DIASTOLIC_BP"] = pd.to_numeric(bp_bmi["DIASTOLIC_BP"], errors='coerce')
bp_bmi["BMI"] = pd.to_numeric(bp_bmi["BMI"], errors='coerce')

# Check shapes of the relevant data to ensure they are 1D
print("\n--- Checking Shapes of Data ---")
print(f"Shape of Systolic BP: {bp_bmi['SYSTOLIC_BP'].dropna().shape}")
print(f"Shape of BMI: {bp_bmi['BMI'].dropna().shape}")

# Plotting
# Ensure we pass numpy arrays for the KDE plot
plt.figure(figsize=(14, 7))

# For faster plotting, sample a subset of data (e.g., 10% of the data)
sample_size = 0.1
hyper_sample = bp_bmi[bp_bmi["HYPERTENSIVE"]].sample(frac=sample_size, random_state=42)
nonhyper_sample = bp_bmi[~bp_bmi["HYPERTENSIVE"]].sample(frac=sample_size, random_state=42)

# Convert the SYSTOLIC_BP column to a numpy array and flatten it
hypertensive_systolic_bp = np.ravel(hyper_sample["SYSTOLIC_BP"].dropna().values)
non_hypertensive_systolic_bp = np.ravel(nonhyper_sample["SYSTOLIC_BP"].dropna().values)

# Plotting the density plots
sns.kdeplot(hypertensive_systolic_bp, label="Hypertensive", color="red")
sns.kdeplot(non_hypertensive_systolic_bp, label="Non-Hypertensive", color="blue")

plt.title("Systolic BP Distribution (Sampled Data)")
plt.xlabel("Systolic BP")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()

# BMI Plot
plt.figure(figsize=(14, 7))
sns.kdeplot(np.ravel(hyper_sample["BMI"].dropna().values), label="Hypertensive", color="red")
sns.kdeplot(np.ravel(nonhyper_sample["BMI"].dropna().values), label="Non-Hypertensive", color="blue")
plt.title("BMI Distribution (Sampled Data)")
plt.xlabel("BMI")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()

