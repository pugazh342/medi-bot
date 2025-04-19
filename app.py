import streamlit as st
from chatbot_logic import load_data, get_medical_response, detect_urgency

# Step 1: Load the Data
symptom_mapping = load_data("data")

# Step 2: Set up the Streamlit app configuration
st.set_page_config(page_title="Medical Assistance Chatbot", page_icon="🩺", layout="centered")

# Display the chatbot title and description
st.title("💬 Medical Assistance Chatbot")
st.markdown("Describe your symptoms, and I’ll try to help you understand what it might be.")


# History of conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.text_input("How are you feeling today?", placeholder="e.g., I have chest pain and fever")
# Symptom picker(multi-select)
symptom_list = list(symptom_mapping.keys())
selected_symptoms = st.multiselect("Or select symptoms manually:", symptom_list)
# Combine text input and symptom picker
combined_input = user_input.strip()
if selected_symptoms:
    selected_text = ", ".join(selected_symptoms)
    if combined_input:
        combined_input += ", " + selected_text
    else:
        combined_input = selected_text
# Process input
if user_input:
    if detect_urgency(combined_input):
        st.error("🚨 This may be a medical emergency. Please seek immediate medical attention.")
    
    response = get_medical_response(user_input, symptom_mapping)

    # Save conversation
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display conversation
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")


# Step 5: Footer
st.markdown("---")
st.markdown("🛟 _Note: This chatbot provides basic information and is not a substitute for professional medical advice. Please consult a healthcare professional for accurate diagnosis and treatment._")
