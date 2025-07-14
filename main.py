import streamlit as st
import speech_recognition as sr
import threading

# Page settings
st.set_page_config(page_title="Adaptify Speech-to-Text", page_icon="🎙️", layout="centered")

st.title("🎙️ Adaptify - Speech-to-Text Demo")

recognizer = sr.Recognizer()

# Session states
if "history" not in st.session_state:
    st.session_state.history = []

if "is_listening" not in st.session_state:
    st.session_state.is_listening = False


def listen_in_background():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while st.session_state.is_listening:
            with st.spinner("Listening..."):
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio)
                    st.session_state.history.append(text)
                except sr.UnknownValueError:
                    st.session_state.history.append("[Could not understand]")
                except sr.RequestError as e:
                    st.session_state.history.append(f"[API Error: {e}]")


def start_listening():
    if not st.session_state.is_listening:
        st.session_state.is_listening = True
        threading.Thread(target=listen_in_background).start()


def stop_listening():
    st.session_state.is_listening = False


def clear_history():
    st.session_state.history.clear()


# Layout Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎙️ Start Listening"):
        start_listening()
with col2:
    if st.button("⏹️ Stop Listening"):
        stop_listening()
with col3:
    if st.button("🧹 Clear History"):
        clear_history()

# Display Text History
st.subheader("📝 Recognized Text History")
if st.session_state.history:
    st.text_area("History:", "\n".join(st.session_state.history), height=300, label_visibility="collapsed")
else:
    st.info("No recognized text yet.")


# Optional: Status
status = "Listening..." if st.session_state.is_listening else "Stopped"
st.write(f"**Status:** {status}")
