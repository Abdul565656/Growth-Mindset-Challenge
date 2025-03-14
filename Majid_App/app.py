import streamlit as st
import speech_recognition as sr
import pyttsx3
import arabic_reshaper
import bidi.algorithm
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sounddevice as sd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Virtual Imam Assistant",
    page_icon="🕌",
    layout="wide"
)

# Initialize speech recognition
r = sr.Recognizer()

def initialize_tts():
    engine = pyttsx3.init()
    return engine

def format_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = bidi.algorithm.get_display(reshaped_text)
    return bidi_text

def main():
    st.title("Virtual Imam Assistant 🕌")
    st.markdown("""
    ### Welcome to the Virtual Imam Assistant
    This application helps monitor Quran recitation during Taraweeh prayers and provides corrections when needed.
    """)

    # Sidebar
    st.sidebar.header("Settings")
    sensitivity = st.sidebar.slider("Correction Sensitivity", 0.0, 1.0, 0.8)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recitation Monitor")
        if st.button("Start Listening"):
            with st.spinner("Listening to recitation..."):
                try:
                    with sr.Microphone() as source:
                        st.info("Adjusting for ambient noise... Please wait.")
                        r.adjust_for_ambient_noise(source, duration=2)
                        st.success("Ready! Please begin recitation.")
                        audio = r.listen(source, timeout=10, phrase_time_limit=30)
                        
                        try:
                            text = r.recognize_google(audio, language='ar-AR')
                            st.write("Recognized text:", format_arabic_text(text))
                            
                            # Here you would implement the Quran verification logic
                            # For demonstration, we'll just show the recognized text
                            
                        except sr.UnknownValueError:
                            st.error("Could not understand the recitation")
                        except sr.RequestError as e:
                            st.error(f"Error with the speech recognition service; {e}")
                except Exception as e:
                    st.error(f"Error accessing microphone: {e}")
    
    with col2:
        st.subheader("Quran Reference")
        # Add a text area for the expected Quran verses
        expected_verses = st.text_area(
            "Enter expected verses (for reference)",
            height=200
        )
        
        if expected_verses:
            st.markdown("### Formatted Arabic Text:")
            st.write(format_arabic_text(expected_verses))

    # Footer
    st.markdown("---")
    st.markdown("""
    #### How to use:
    1. Enter the expected verses in the reference section
    2. Click "Start Listening" when ready to begin
    3. Recite the verses
    4. The system will monitor and provide corrections if needed
    """)

if __name__ == "__main__":
    main() 