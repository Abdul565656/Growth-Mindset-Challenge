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
from quran_verifier import QuranVerifier
import re
import threading

# Initialize global variables first
engine = None
expected_verses = ""
is_listening = False

# Set page config
st.set_page_config(
    page_title="Virtual Muqtadi Assistant",
    page_icon="🕌",
    layout="wide"
)

# Initialize speech recognition and text-to-speech with better error handling
r = sr.Recognizer()

try:
    engine = pyttsx3.init()
    # Configure the engine
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    # Test the engine at startup
    def test_tts():
        try:
            engine.say("System ready")
            engine.runAndWait()
            st.success("Text-to-speech system initialized successfully")
        except Exception as e:
            st.error(f"Text-to-speech test failed: {e}")
            
    # Run the test in a thread to avoid blocking
    threading.Thread(target=test_tts).start()
except Exception as e:
    st.error(f"Failed to initialize text-to-speech engine: {e}")

def clean_arabic_text(text):
    # Remove diacritics and special characters
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # Remove tashkeel
    text = re.sub(r'[^\u0621-\u063A\u0641-\u064A\s]', '', text)  # Keep only Arabic letters and spaces
    return text.strip()

def speak_correction(text, rate=150):
    global engine
    if engine is None:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            engine.setProperty('volume', 1.0)
        except Exception as e:
            st.error(f"Could not initialize text-to-speech engine: {e}")
            return
        
    try:
        st.info(f"Speaking correction: {text}")  # Debug message
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 1.0)
        
        # Break the text into smaller chunks for better reliability
        words = text.split()
        for i in range(0, len(words), 3):
            chunk = " ".join(words[i:i+3])
            engine.say(chunk)
            engine.runAndWait()
            time.sleep(0.1)  # Small pause between chunks
            
        st.success("Correction spoken successfully")  # Debug message
    except Exception as e:
        st.error(f"Error speaking correction: {e}")
        # Try to reinitialize the engine
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            engine.setProperty('volume', 1.0)
        except Exception as e2:
            st.error(f"Failed to reinitialize speech engine: {e2}")

def format_arabic_text(text):
    # Clean the text first
    text = clean_arabic_text(text)
    # Reshape for proper display
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = bidi.algorithm.get_display(reshaped_text)
    return bidi_text

def get_next_expected_words(current_position, full_text, num_words=5):
    words = full_text.split()
    if current_position >= len(words):
        return ""
    end_pos = min(current_position + num_words, len(words))
    return " ".join(words[current_position:end_pos])

def listen_to_recitation(source, placeholder, verifier, expected_text):
    global is_listening
    is_listening = True
    
    # Clean and prepare the expected text
    expected_text = clean_arabic_text(expected_text)
    words = expected_text.split()
    current_word_position = 0
    
    # Adjust for ambient noise
    placeholder.info("Adjusting microphone for background noise... Please wait.")
    r.adjust_for_ambient_noise(source, duration=2)
    
    # Set recognition parameters
    r.dynamic_energy_threshold = True
    r.energy_threshold = 1000  # Lower threshold for better sensitivity
    r.pause_threshold = 1.0  # More forgiving pause threshold
    r.phrase_threshold = 0.3  # More sensitive to phrase starts
    r.non_speaking_duration = 0.5  # Shorter duration for non-speaking detection
    
    placeholder.success("Ready! Start reciting, and I'll help when needed.")
    
    # Show the complete surah for reference
    with st.sidebar:
        st.markdown("### Complete Surah Reference:")
        st.markdown(f"<div dir='rtl' style='font-size: 18px; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(expected_text)}</div>", unsafe_allow_html=True)
    
    try:
        while is_listening and current_word_position < len(words):
            try:
                # Listen without timeout for the start of speech
                audio = r.listen(source, timeout=None, phrase_time_limit=5)
                
                try:
                    # Recognize the recitation
                    text = r.recognize_google(audio, language='ar-SA')
                    cleaned_text = clean_arabic_text(text)
                    
                    # Get the expected next few words
                    expected_segment = get_next_expected_words(current_word_position, expected_text)
                    
                    # Verify recitation
                    is_correct, similarity = verifier.verify_recitation(cleaned_text, expected_segment)
                    
                    # Show current status
                    placeholder.markdown("### Current Recitation:")
                    placeholder.markdown(f"<div dir='rtl' style='font-size: 24px; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(cleaned_text)}</div>", unsafe_allow_html=True)
                    
                    if similarity < 0.3:  # Significant difference detected
                        # Immediately provide the correct continuation
                        placeholder.warning("Correction:")
                        placeholder.markdown(f"<div dir='rtl' style='font-size: 24px; color: #1e88e5; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(expected_segment)}</div>", unsafe_allow_html=True)
                        
                        # Speak the correction immediately in a separate thread
                        correction_thread = threading.Thread(target=speak_correction, args=(expected_segment,))
                        correction_thread.start()
                    elif is_correct:
                        current_word_position += len(cleaned_text.split())
                        # Show next expected words
                        next_segment = get_next_expected_words(current_word_position, expected_text)
                        if next_segment:
                            placeholder.info("Next words:")
                            placeholder.markdown(f"<div dir='rtl' style='font-size: 24px; color: #4CAF50; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(next_segment)}</div>", unsafe_allow_html=True)
                    
                except sr.UnknownValueError:
                    # No speech detected, show the next expected segment
                    expected_segment = get_next_expected_words(current_word_position, expected_text)
                    placeholder.info("Continue with:")
                    placeholder.markdown(f"<div dir='rtl' style='font-size: 24px; color: #1e88e5; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(expected_segment)}</div>", unsafe_allow_html=True)
                    
                except sr.RequestError as e:
                    placeholder.error(f"Could not request results; {e}")
                    break
                    
            except sr.WaitTimeoutError:
                # Timeout occurred, just continue listening
                continue
                
    except Exception as e:
        placeholder.error(f"Error: {e}")
    finally:
        is_listening = False
        placeholder.info("Listening stopped. Click 'Start Listening' to begin again.")

def main():
    global expected_verses, is_listening
    
    st.title("Virtual Muqtadi Assistant 🕌")
    st.markdown("""
    ### Welcome to the Virtual Muqtadi Assistant
    This application helps with Quran recitation by providing immediate voice corrections when needed.
    """)

    # Sidebar
    st.sidebar.header("Settings")
    sensitivity = st.sidebar.slider("Correction Sensitivity", 0.0, 1.0, 0.3)  # More lenient default
    
    # Initialize Quran verifier
    verifier = QuranVerifier(sensitivity=sensitivity)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col2:
        st.subheader("Surah Reference")
        st.markdown("""
        Enter the surah or verses you will recite.
        Example:
        ```
        بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
        الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
        ```
        """)
        expected_verses = st.text_area(
            "Enter the verses",
            height=200,
            help="Enter the verses you will recite"
        )
        
        if expected_verses:
            st.markdown("### Preview:")
            st.markdown(
                f"<div dir='rtl' style='font-size: 24px; font-family: \"Traditional Arabic\", Arial;'>{format_arabic_text(expected_verses)}</div>",
                unsafe_allow_html=True
            )
    
    with col1:
        st.subheader("Recitation Monitor")
        placeholder = st.empty()
        
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            if st.button("Start Listening", type="primary", disabled=is_listening):
                if not expected_verses:
                    st.error("Please enter the verses first.")
                else:
                    try:
                        with sr.Microphone() as source:
                            listen_to_recitation(source, placeholder, verifier, expected_verses)
                    except Exception as e:
                        st.error(f"Error accessing microphone: {e}")
        
        with col1_2:
            if st.button("Stop Listening", type="secondary", disabled=not is_listening):
                is_listening = False
                placeholder.info("Listening stopped.")

    # Footer
    st.markdown("---")
    st.markdown("""
    #### How to use:
    1. Enter the verses you will recite
    2. Click "Start Listening"
    3. Begin reciting - the system will automatically:
       - Show the next words you should recite
       - Provide corrections if needed
       - Give voice feedback for corrections
    4. Click "Stop Listening" when done
    
    #### Tips:
    - Wait for the "Ready!" message before starting
    - Speak clearly and at a natural pace
    - The system will show you the next words to recite
    - If you need help, just pause and the system will assist
    - Make sure your microphone is working and selected
    """)

if __name__ == "__main__":
    main() 