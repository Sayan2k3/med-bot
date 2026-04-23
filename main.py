# medi_bot_app.py

import os
import streamlit as st
import google.generativeai as genai


# 🎯 Gemini API Configuration
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing Gemini API Key. Please configure GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)

# -----------------------------
# ⚙️ Gemini Model Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    "gemini-flash-latest",
    generation_config=generation_config,
)


# -----------------------------
# 🧠 Initial Chat Context
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are a Medi-bot and can answer health-related queries and suggest health insurance plans and customized diet plans for people in India. Respond appropriately to medical queries, insurance suggestions, and personalized situations. Be conversational, informative, and polite."
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Namaste! I'm Medi-bot, your friendly AI health assistant. I can help you with:\n\n- Health-related queries\n- Customized diet plans\n- India-based health insurance recommendations\n\nPlease go ahead and tell me what you need help with!"
                ],
            },
        ]
    )

# -----------------------------
# 🌟 Streamlit UI Design
st.set_page_config(page_title="Medi-Bot - Your Health AI Agent", page_icon="🩺")

st.markdown(
    """
    <div style="text-align:center">
        <h1 style="color:#008080;">🤖 MEDI-BOT</h1>
        <p style="font-size:20px;">👨‍⚕️ Your Health-AI Agent is here — Ask your medical, insurance or diet-related queries!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 💬 Chat Interface
user_input = st.chat_input("Type your query here...")

# Display chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(entry["user"])
    with st.chat_message("assistant"):
        st.markdown(entry["bot"])

# -----------------------------
# 🚀 Send and Display Response
if user_input:
    st.chat_message("user").markdown(user_input)

    try:
        response = st.session_state.chat_session.send_message(user_input)
        bot_response = response.text
        st.chat_message("assistant").markdown(bot_response)
        
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": bot_response
        })
    except Exception as e:
        st.error(f"Error communicating with AI: {str(e)}")
