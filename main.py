import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

st.set_page_config(page_title="Speech-to-Text App", layout="centered")
st.title("🎙️ Speech-to-Text App (Upload any audio file)")

uploaded_file = st.file_uploader(
    "Upload an audio file (wav, mp3, m4a, flac, ogg, aac)", 
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

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_temp.name) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("✅ Recognized Text:")
            st.text_area("Transcript:", value=text, height=200)
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ API Error: {e}")

    # Clean up temp files
    os.unlink(temp_audio_path)
    os.unlink(wav_temp.name)

# Clear history button (optional)
clear = st.button("Clear Transcript")
if clear:
    st.session_state.clear()
    st.rerun()

