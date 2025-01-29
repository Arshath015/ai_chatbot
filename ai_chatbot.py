import streamlit as st
import google.generativeai as generativeai

# Load API Key from Streamlit Secrets
if "google" not in st.secrets:
    st.error("⚠️ API Key is missing! Please set it in Streamlit Secrets.")
    st.stop()

Google_API_KEY = st.secrets["google"]["api_key"]

# Configure Google Gemini AI
generativeai.configure(api_key=Google_API_KEY)

# Sidebar Component
def st_sidebar():
    with st.sidebar:
        st.title("AI Chatbot")
        st.text("Feel free to ask me anything! 😊")
        rate = st.slider("How much do you rate our App?", 0, 5, 0, step=1)
        if rate > 0:
            st.write("Thank you for your feedback! 🎉")

# Function to display chat messages
def display_message(role, text):
    """Display messages with distinct styles for User and Assistant."""
    color = "#0d6efd" if role == "user" else "#198754"
    align = "right" if role == "user" else "left"

    st.markdown(
        f"""
        <div style="display: flex; justify-content: {align}; margin: 5px 0;">
            <div style="background-color: {color}; color: white; padding: 12px; 
                        border-radius: 10px; max-width: 70%; font-size: 16px;">
                <strong>{role.upper()}:</strong> {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Chat Session Management
def session(session_key, user_prompt):
    """Handle chat session and display user & bot messages properly."""
    for message in st.session_state[session_key].history:
        role = "user" if message.role == "user" else "assistant"
        message_text = message.parts[0].text
        display_message(role, message_text)

    if user_prompt:
        display_message("user", user_prompt)

        # AI Response
        try:
            response = st.session_state[session_key].send_message(user_prompt)
            if response.candidates:
                assistant_text = response.candidates[0].content.parts[0].text
                display_message("assistant", assistant_text)
            else:
                st.error("No valid response from AI.")
        except Exception as e:
            st.error(f"Error during AI response: {e}")

# Main Function
def main():
    st.set_page_config(
        page_title="AI Chatbot",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("🤖 AI ChatBot using Google Gemini")

    llm = generativeai.GenerativeModel("gemini-pro")
    st_sidebar()

    # Initialize chat session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = llm.start_chat(history=[])

    user_prompt = st.chat_input("Ask me anything...")
    if user_prompt is not None:
        session("chat_session", user_prompt=user_prompt)

# Run the main function
if __name__ == "__main__":
    main()
