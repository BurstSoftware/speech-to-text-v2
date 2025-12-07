import streamlit as st
import speech_recognition as sr
import tempfile
import time

r = sr.Recognizer()

def speech_to_text_from_bytes(audio_bytes):
    # Save the audio bytes to a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Google Speech API error: {str(e)}"


def main():
    st.title("🎤 Voice Input + Chat Input App")

    if "text" not in st.session_state:
        st.session_state.text = ""

    st.subheader("🎙 Record Your Voice")

    audio = st.audio_input("Press to Record Your Voice")

    if audio is not None:
        with st.spinner("Transcribing..."):
            text = speech_to_text_from_bytes(audio.getvalue())
            st.session_state.text = text

    if st.session_state.text:
        st.subheader("📝 Transcribed Text")
        st.write(st.session_state.text)

    if st.button("Clear"):
        st.session_state.text = ""

    st.markdown("---")
    st.subheader("💬 Chat Input (optional)")
    user_msg = st.chat_input("Type something here...")

    if user_msg:
        st.write(f"**You typed:** {user_msg}")


if __name__ == "__main__":
    main()
