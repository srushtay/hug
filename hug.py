import streamlit as st
import requests

# Set your Hugging Face Token here!
api_token = ""  # <-- Your real token here

# Function to query models
def ask_model_api(model_name, prompt):
    model_endpoints = {
        "LLaMA": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
        "Mistral": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        "Falcon": "https://api-inference.huggingface.co/models/bigscience/bloomz-560m",
        "Grok": "simulate",
    }


    if model_name not in model_endpoints:
        return "Model not supported."

    if model_name == "Grok":
        return "This is a simulated Grok answer."

    api_url = model_endpoints[model_name]

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    if model_name == "Vicuna":
        # For OpenRouter API (Vicuna type), special payload
        payload = {
            "model": "vicuna-7b-v1.5-16k",
            "messages": [{"role": "user", "content": prompt}]
        }
    else:
        # For Huggingface models like LLaMA, Falcon, Mistral
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 300,
                "return_full_text": False
            }
        }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code} {response.text}"
        result = response.json()

        if model_name == "Vicuna":
            return result['choices'][0]['message']['content']
        else:
            return result[0]['generated_text']

    except Exception as e:
        return f"Error: {str(e)}"

# ----------------- Streamlit UI Part -----------------

st.set_page_config(page_title="Chat with Your Favorite Model", layout="wide")
st.title("Chat with Your Favorite Model")

# Sidebar Model Selection
model_choice = st.sidebar.selectbox(
    "Choose a Model:",
    ["LLaMA", "Mistral", "Falcon", "Grok"]
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text Input
user_prompt = st.text_input("Enter your prompt:")

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Send"):
        if user_prompt:
            with st.spinner("Waiting for model response..."):
                response = ask_model_api(model_choice, user_prompt)
                st.session_state.chat_history.append(("🧑 You", user_prompt))
                st.session_state.chat_history.append(("🤖 " + model_choice, response))
        else:
            st.warning("Please enter a prompt.")

with col2:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Display Chat History
st.markdown("---")
for sender, message in st.session_state.chat_history:
    if sender.startswith("🧑"):
        st.markdown(
            f"<div style='background-color: #DCF8C6; padding:10px; border-radius:10px; margin:5px 0;'><strong>{sender}:</strong> {message}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color: #F1F0F0; padding:10px; border-radius:10px; margin:5px 0;'><strong>{sender}:</strong> {message}</div>",
            unsafe_allow_html=True
        )
