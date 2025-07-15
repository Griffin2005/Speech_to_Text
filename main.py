import streamlit as st
import speech_recognition as sr
import io

st.title("Speech to Text Demo 🎙️")

# Initialize session state for transcript
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

uploaded_file = st.file_uploader("Upload an Audio File (.wav, .mp3)", type=["wav", "mp3", "ogg", "flac"])

if uploaded_file:
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(io.BytesIO(uploaded_file.read()))

    with audio_data as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        st.session_state.transcript += text + "\n"
    except sr.UnknownValueError:
        st.session_state.transcript += "Could not understand audio.\n"
    except sr.RequestError as e:
        st.session_state.transcript += f"API error: {e}\n"

# Show current transcript
st.subheader("Transcript:")
st.text_area("Recognized Speech", st.session_state.transcript, height=200)

# Clear button
if st.button("Clear Transcript"):
    st.session_state.transcript = ""
    st.rerun()
