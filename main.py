import streamlit as st
import speech_recognition as sr
import os
from pydub import AudioSegment  # For converting m4a to wav
from io import BytesIO

st.title("Speech to Text (Supports .wav and .m4a)")

uploaded_file = st.file_uploader("Upload an audio file (.wav or .m4a)", type=["wav", "m4a"])

if uploaded_file:
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
    st.write(file_details)

    # Convert .m4a to .wav if needed
    if uploaded_file.name.endswith(".m4a"):
        audio = AudioSegment.from_file(uploaded_file, format="m4a")
        buffer = BytesIO()
        audio.export(buffer, format="wav")
        buffer.seek(0)
        audio_file = sr.AudioFile(buffer)
    else:
        audio_file = sr.AudioFile(uploaded_file)

    recognizer = sr.Recognizer()
    with audio_file as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Recognized Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"API Error: {e}")
