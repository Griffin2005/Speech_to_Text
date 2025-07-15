import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
from io import BytesIO

st.title("Speech-to-Text with Any Audio Format")

uploaded_file = st.file_uploader(
    "Upload your audio file (mp3, wav, m4a, flac, ogg, aac)", 
    type=["wav", "mp3", "m4a", "flac", "ogg", "aac"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    file_extension = uploaded_file.name.split(".")[-1].lower()

    # Write uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Convert it to WAV using pydub
    audio = AudioSegment.from_file(temp_audio_path)
    wav_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(wav_temp.name, format="wav")

    # Speech Recognition on WAV file
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_temp.name) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Recognized Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"API Error: {e}")

    # Clean up temp files
    os.unlink(temp_audio_path)
    os.unlink(wav_temp.name)
