# 09_hypertension_prevalence.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
print("Loading data...")
patients = pd.read_csv("data/original/patients.csv.gz")
conditions = pd.read_csv("data/original/conditions.csv.gz")
observations = pd.read_csv("data/original/observations.csv.gz")

print("\n--- Sample of Conditions ---")
print(conditions.head())

# Update hypertension codes from sample
hypertension_codes = {"10509002", "283371005", "444814009", "16114001"}

conditions["CODE"] = conditions["CODE"].astype(str).str.rstrip(".0")


print("\nIdentifying hypertensive patients...")
hypertensive_patients = conditions[conditions["CODE"].isin(hypertension_codes)]["PATIENT"].unique()
print("Number of hypertensive patients:", len(hypertensive_patients))

print("\n--- Summary: Blood Pressure ---")

bp_codes = {"8480-6": "SYSTOLIC_BP", "8462-4": "DIASTOLIC_BP"}
bmi_code = "39156-5"

# Filter and clean observations
bp_obs = observations[observations["CODE"].isin(bp_codes.keys())].copy()
bmi_obs = observations[observations["CODE"] == bmi_code].copy()

bp_obs["VALUE"] = pd.to_numeric(bp_obs["VALUE"], errors="coerce")
bmi_obs["VALUE"] = pd.to_numeric(bmi_obs["VALUE"], errors="coerce")

# Pivot BP
bp_wide = bp_obs.pivot_table(index=["PATIENT", "DATE"], 
                              columns="CODE", values="VALUE", aggfunc="mean").reset_index()
bp_wide.rename(columns=bp_codes, inplace=True)

bmi_clean = bmi_obs[["PATIENT", "DATE", "VALUE"]].rename(columns={"VALUE": "BMI"})

# Merge and tag
data = pd.merge(bp_wide, bmi_clean, on=["PATIENT", "DATE"], how="outer")
data["HYPERTENSION"] = data["PATIENT"].isin(hypertensive_patients)

# Split and clean
hyper = data[data["HYPERTENSION"] == True].copy()
non_hyper = data[data["HYPERTENSION"] == False].copy()

for df in [hyper, non_hyper]:
    df["SYSTOLIC_BP"] = pd.to_numeric(df["SYSTOLIC_BP"], errors="coerce")
    df["DIASTOLIC_BP"] = pd.to_numeric(df["DIASTOLIC_BP"], errors="coerce")
    df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce")

# Summary stats
print("\nHypertensive BP:\n", hyper[["SYSTOLIC_BP", "DIASTOLIC_BP"]].describe())
print("\nNon-Hypertensive BP:\n", non_hyper[["SYSTOLIC_BP", "DIASTOLIC_BP"]].describe())

print("\n--- Summary: BMI ---")
print("\nHypertensive BMI:\n", hyper["BMI"].describe())
print("\nNon-Hypertensive BMI:\n", non_hyper["BMI"].describe())

# --- Plots ---
# Explicitly convert data to a 1D NumPy array using np.ravel()
import numpy as np


sns.kdeplot(np.array(hyper["SYSTOLIC_BP"].dropna()), label="Hypertensive", color="red")
sns.kdeplot(np.array(non_hyper["SYSTOLIC_BP"].dropna()), label="Non-Hypertensive", color="blue")


plt.title("Systolic Blood Pressure Distribution")
plt.xlabel("Systolic BP (mmHg)")
plt.legend()
plt.show()

sns.kdeplot(hyper["DIASTOLIC_BP"].dropna().values, label="Hypertensive", color="red")
sns.kdeplot(non_hyper["DIASTOLIC_BP"].dropna().values, label="Non-Hypertensive", color="blue")
plt.title("Diastolic Blood Pressure Distribution")
plt.xlabel("Diastolic BP (mmHg)")
plt.legend()
plt.show()

sns.kdeplot(hyper["BMI"].dropna().values, label="Hypertensive", color="red")
sns.kdeplot(non_hyper["BMI"].dropna().values, label="Non-Hypertensive", color="blue")
plt.title("BMI Distribution")
plt.xlabel("BMI (kg/m²)")
plt.legend()
plt.show()


# --- Crude prevalence ---
print("\n--- Crude Prevalence of Hypertension ---")
total_patients = patients["Id"].nunique()
crude_prevalence = len(hypertensive_patients) / total_patients
print(f"Crude prevalence: {crude_prevalence:.2%}")

# --- Adjusted prevalence ---
print("\n--- Adjusted Prevalence (Placeholder) ---")
print("Adjusted prevalence estimation requires UK population age distribution.")

