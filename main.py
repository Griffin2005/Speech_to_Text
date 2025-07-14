from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr
import streamlit as st

st.title("Speech-to-Text: Multi-Format Audio Support (.mp3, .m4a, .ogg, .wav, etc.)")

uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "m4a", "flac", "ogg", "aac"])

if uploaded_file:
    st.write(f"File Uploaded: {uploaded_file.name}")
    
    # Extract format from extension
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Convert all to WAV
    audio = AudioSegment.from_file(uploaded_file, format=file_extension)
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Recognized Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"API Error: {e}")
