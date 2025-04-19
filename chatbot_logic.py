import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

# Step 1: Load the Data
def load_data(data_folder="data"):
    all_dataframes = []
    
    # Loop through the CSV files and load them
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_folder, filename)
            df = pd.read_csv(file_path)
            all_dataframes.append(df)

    # Combine the CSVs into one DataFrame
    full_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Extract relevant columns: Symptoms, Diagnosis, Medication
    symptom_data = full_df[["Symptoms", "Diagnosis", "Medication"]].dropna()

    # Build a dictionary mapping symptoms to their diagnosis and recommendations
    symptom_mapping = {}
    for _, row in symptom_data.iterrows():
        symptoms = [s.strip().lower() for s in row["Symptoms"].split(",")]
        for symptom in symptoms:
            if symptom not in symptom_mapping:
                symptom_mapping[symptom] = {
                    "condition": row["Diagnosis"],
                    "recommendation": f"Suggested medication: {row['Medication']}"
                }
    
    return symptom_mapping
URGENT_SYMPTOMS = [
    "chest pain", "shortness of breath", "severe headache", "loss of consciousness",
    "numbness", "slurred speech", "high fever", "seizure"
]

def detect_urgency(user_input):
    for symptom in URGENT_SYMPTOMS:
        if symptom in user_input.lower():
            return True
    return False

# Step 2: Generate Medical Response based on User Input
def get_medical_response(user_input, mapping):
    user_input = user_input.lower()
    matched = []

    for symptom, data in mapping.items():
        if symptom in user_input or fuzz.partial_ratio(symptom, user_input) > 70:
            matched.append((symptom, data["condition"], data["recommendation"]))

    if not matched:
        return "🤔 I'm not sure about that. Could you provide more details or different symptoms?"

    response = "🩺 Based on what you said, here’s what I found:\n\n"
    for symptom, condition, recommendation in matched:
        response += f"- **{symptom.capitalize()}** → _{condition}_\n  {recommendation}\n\n"

    return response.strip()

