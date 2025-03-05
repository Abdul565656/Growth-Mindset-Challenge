import streamlit as st
import requests
import datetime
import time
import random

# Set Page Configuration
st.set_page_config(page_title="Prayers App", page_icon="🕌", layout="centered")

# Custom Styling for Improved UI
custom_theme = """
    <style>
        body { background-color: #121212 !important; color: white !important; font-family: Arial, sans-serif; }
        .stTextInput, .stNumberInput, .stSelectbox, .stButton>button { 
            border-radius: 10px; 
            padding: 10px;
            background-color: #222;
            color: white;
            border: 1px solid #444;
        }
        [data-testid="stSidebar"] {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        h1 { color: #4dabf7; text-align: center; font-size: 36px; }
        h2 { color: #4dabf7; text-align: center; font-size: 28px; }
        .stMarkdown { text-align: center; }
        .prayer-time {
            background-color: #1e1e1e;
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
"""
st.markdown(custom_theme, unsafe_allow_html=True)

# Sidebar - Auto-detect Location or Manual Input
st.sidebar.header("⚙️ Settings")
auto_location = st.sidebar.checkbox("Auto-detect Location", value=True)

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        return response["city"], response["country"]
    except:
        return "Makkah", "Saudi Arabia"

city, country = get_location() if auto_location else (
    st.sidebar.text_input("Enter City", "Makkah"),
    st.sidebar.text_input("Enter Country", "Saudi Arabia")
)

# Fetch Prayer Times
def get_prayer_times(city, country):
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
    response = requests.get(url).json()
    return response['data']['timings'], response['data']['date']['hijri']

prayer_times, hijri_date = get_prayer_times(city, country)

# Only Farz Prayers
farz_prayers = {"Fajr": prayer_times["Fajr"], "Dhuhr": prayer_times["Dhuhr"], "Asr": prayer_times["Asr"], "Maghrib": prayer_times["Maghrib"], "Isha": prayer_times["Isha"]}

# Main App
st.markdown("<h1>🕌 Prayers App By Abdullah Kashif</h1>", unsafe_allow_html=True)
st.markdown(f"<h2>📆 Hijri Date: {hijri_date['day']} {hijri_date['month']['en']} {hijri_date['year']}</h2>", unsafe_allow_html=True)

# Display Prayer Times
st.markdown("<h2>📅 Today's Prayer Times</h2>", unsafe_allow_html=True)

for prayer, time in farz_prayers.items():
    st.markdown(f'<div class="prayer-time"><strong>{prayer}</strong>: {time}</div>', unsafe_allow_html=True)

# Countdown Timer for Next Prayer
now = datetime.datetime.now()
upcoming_prayer = None
for prayer, time in farz_prayers.items():
    prayer_time = datetime.datetime.strptime(time, "%H:%M").time()
    if now.time() < prayer_time:
        upcoming_prayer = (prayer, time)
        break

if upcoming_prayer:
    prayer_time = datetime.datetime.strptime(upcoming_prayer[1], "%H:%M").time()
    prayer_datetime = datetime.datetime.combine(now.date(), prayer_time)
    remaining_time = prayer_datetime - now
    st.success(f"⏳ Next Prayer: {upcoming_prayer[0]} at {upcoming_prayer[1]} ({remaining_time})")
else:
    st.success("✅ All prayers for today are completed!")

# Quran Recitation Section
st.markdown("<h2>📖 Listen to Quran Recitation</h2>", unsafe_allow_html=True)

# Default Recitation (You can replace this with a local file or another online URL)
recitation_url = "https://download.quranicaudio.com/quran/abdullaah_3awwaad_al-juhaynee/055.mp3"  # Surah Al-Fatiha by Al-Sudais

if st.button("▶️ Play Recitation"):
    st.audio(recitation_url, format="audio/mp3")

# Footer
st.markdown("<br><center>🌙 Made with ❤️ for Ummah</center>", unsafe_allow_html=True)
