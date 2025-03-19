import streamlit as st
import zxcvbn
import requests
import secrets
import string
import pyperclip

# Function to check password strength
def check_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    entropy = result['guesses_log10']
    
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    strength_colors = ["#FF4B4B", "#FF914D", "#FFC300", "#57C478", "#2BA84A"]
    
    return strength_levels[score], strength_colors[score], feedback['suggestions'], entropy, score

# Function to check if password is leaked
def check_pwned_password(password):
    hashed = requests.get(f"https://api.pwnedpasswords.com/range/{password[:5]}").text
    return password in hashed

# Function to generate a secure password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Streamlit UI
st.title("🔒 Password Strength Meter")
password = st.text_input("Enter your password:", type="password")

if password:
    strength, color, suggestions, entropy, score = check_password_strength(password)
    
    # Display strength with color and progress bar
    st.markdown(f"<h3 style='color: {color};'>Strength: {strength}</h3>", unsafe_allow_html=True)
    st.progress((score + 1) / 5)  # Progress bar (normalized from 0-4 to 0-1)
    st.write(f"🔢 Entropy Score: {entropy:.2f} (Higher is better)")
    
    if suggestions:
        st.warning("Suggestions to improve your password:")
        for suggestion in suggestions:
            st.write(f"🔹 {suggestion}")
    
    if check_pwned_password(password):
        st.error("❌ This password has been found in a data breach! Choose a stronger one.")

# Password Generator
st.subheader("🔑 Generate a Secure Password")
password_length = st.slider("Select password length:", min_value=8, max_value=32, value=12)

if st.button("Generate Password"):
    new_password = generate_password(password_length)
    st.success("✅ Your secure password:")
    st.code(new_password, language="")

   # Styled Copy Button
def copy_to_clipboard(password):
    try:  # Correctly indented
        pyperclip.copy(password)
        st.success("📋 Password copied to clipboard!")
    except pyperclip.PyperclipException:
        st.error("❌ Clipboard access is not supported in this environment. Please copy manually.")

st.button("📋 Copy to Clipboard", on_click=lambda: copy_to_clipboard(new_password))