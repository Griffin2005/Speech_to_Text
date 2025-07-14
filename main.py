import streamlit as st
import speech_recognition as sr
import os

st.set_page_config(page_title="Adaptify - Speech-to-Text Demo", page_icon="📝", layout="centered")
st.title("🎙️ Adaptify - Speech-to-Text from Audio File")

uploaded_file = st.file_uploader("Upload a WAV audio file", type=["wav"])

if uploaded_file is not None:
    file_path = os.path.join("temp_audio.wav")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.audio(file_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.info("Transcribing...")
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success("Transcription Complete:")
            st.text_area("Recognized Text", text, height=200)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"API Error: {e}")

    os.remove(file_path)
