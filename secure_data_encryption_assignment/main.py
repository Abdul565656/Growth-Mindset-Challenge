import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import json
import os
import time

# Constants
DATA_FILE = "secure_data.json"
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 60  # seconds

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def generate_key(passkey: str) -> bytes:
    hash_obj = hashlib.sha256(passkey.encode())
    return Fernet.generate_key()

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.encrypt(text.encode()).decode()

def decrypt_data(ciphertext: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(ciphertext.encode()).decode()

# Load or initialize app state
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0

# Load persistent data
stored_data = load_data()

def login_page():
    st.title("🔐 Login Required")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    if st.button("Login"):
        # For simplicity: any non-empty credentials allow login
        if username and password:
            st.session_state.auth = True
            st.session_state.attempts = 0
            st.session_state.lockout_time = 0
        else:
            st.error("Invalid login.")

def home():
    st.title("🛡️ Secure Data Encryption System")
    option = st.selectbox("Choose an option", ["Store Data", "Retrieve Data"])

    if option == "Store Data":
        store_data_page()
    elif option == "Retrieve Data":
        retrieve_data_page()

def store_data_page():
    st.header("📥 Store Encrypted Data")
    username = st.text_input("Username")
    text = st.text_area("Enter data to encrypt")
    passkey = st.text_input("Enter a passkey", type="password")

    if st.button("Encrypt & Store"):
        if username and text and passkey:
            key = Fernet.generate_key()
            encrypted = encrypt_data(text, key)
            stored_data[username] = {
                "encrypted_text": encrypted,
                "passkey_hash": hash_passkey(passkey),
                "fernet_key": key.decode()
            }
            save_data(stored_data)
            st.success("Data encrypted and stored successfully!")
        else:
            st.warning("Please fill all fields.")

def retrieve_data_page():
    st.header("🔓 Retrieve Encrypted Data")

    if st.session_state.attempts >= MAX_ATTEMPTS:
        remaining = LOCKOUT_DURATION - (time.time() - st.session_state.lockout_time)
        if remaining > 0:
            st.warning(f"Too many failed attempts. Try again in {int(remaining)} seconds.")
            return
        else:
            st.session_state.attempts = 0

    username = st.text_input("Enter your username")
    passkey = st.text_input("Enter your passkey", type="password")

    if st.button("Decrypt"):
        if username in stored_data:
            user_entry = stored_data[username]
            if hash_passkey(passkey) == user_entry["passkey_hash"]:
                try:
                    decrypted = decrypt_data(user_entry["encrypted_text"], user_entry["fernet_key"].encode())
                    st.success("Decrypted Data:")
                    st.code(decrypted)
                    st.session_state.attempts = 0
                except Exception as e:
                    st.error("Decryption failed. Possible key mismatch.")
            else:
                st.session_state.attempts += 1
                st.error("Incorrect passkey.")
                if st.session_state.attempts >= MAX_ATTEMPTS:
                    st.session_state.lockout_time = time.time()
        else:
            st.error("User not found.")

# MAIN CONTROL FLOW
if not st.session_state.auth:
    login_page()
else:
    home()
