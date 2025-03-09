import streamlit as st
import re
import random
import string
import time

# Page Configuration
st.set_page_config(page_title="🔐 Password Strength Meter",
                   page_icon="🔒", layout="wide")

# Custom Styles
st.markdown("""
    <style>
        body {background-color: #0e1117; color: white;}
        .stTextInput > div > div > input {font-size: 18px; padding: 10px;}
        .password-box {border: 2px solid #FF4B4B; padding: 10px; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Session state to store password history
if "password_history" not in st.session_state:
    st.session_state["password_history"] = []

# Function to generate a strong password
def generate_strong_password(length=12):
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all character types.")

    # Ensure at least one of each required character type
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")

    # Fill the rest randomly
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining = "".join(random.choice(all_characters) for _ in range(length - 4))

    # Shuffle to avoid predictable patterns
    password = list(upper + lower + digit + special + remaining)
    random.shuffle(password)

    return "".join(password)

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Common weak passwords blacklist
    COMMON_PASSWORDS = {"123456", "password", "qwerty", "admin123", "iloveyou"}

    # Blacklist Check
    if password in COMMON_PASSWORDS:
        return "❌ Too common! Choose a stronger password.", "Weak", 0

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔴 At least 8 characters required.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🟠 Include both uppercase & lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🟡 Add at least one number.")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🟢 Include at least one special character.")

    # Strength Level
    strength_levels = ["Weak", "Moderate", "Strong", "Very Strong"]
    strength = strength_levels[score] if score < len(strength_levels) else "Very Strong"

    # Store history
    st.session_state["password_history"].append((password, strength, time.strftime("%H:%M:%S")))

    return feedback, strength, score

# UI Layout
st.title("🔐 Password Strength Meter")
st.subheader("Check your password security and generate strong passwords.")

# Sidebar
with st.sidebar:
    st.header("💡 Password Tips")
    st.markdown("✅ **Use at least 8 characters**")
    st.markdown("✅ **Include uppercase & lowercase letters**")
    st.markdown("✅ **Add at least one number**")
    st.markdown("✅ **Use special characters (!@#$%^&*)**")
    st.divider()

    # Generate Strong Password
    if st.button("🎲 Generate Strong Password"):
        strong_password = generate_strong_password()
        st.success(f"**Generated Password:** `{strong_password}`")

st.markdown("---")

# Password Input
password = st.text_input("🔑 Enter your password:", type="password")

# Check Strength Button
if st.button("🛡️ Check Strength"):
    if password:
        feedback, strength, score = check_password_strength(password)

        # Progress bar (visual strength meter)
        progress_color = ["#FF4B4B", "#FFA500", "#FFD700", "#4CAF50", "#008000"]
        score = min(score, 4)
        st.markdown(f"<div style='background-color: {progress_color[score]}; padding: 10px; border-radius: 5px; color: white; text-align: center; font-weight: bold;'>🔹 Password Strength: {strength}</div>", unsafe_allow_html=True)
        st.progress(score / 4.0)

        # Feedback
        for item in feedback:
            st.warning(item)
    else:
        st.warning("⚠️ Please enter a password!")

st.markdown("---")

# Password History
if st.session_state["password_history"]:
    st.subheader("📜 Password History")
    history_data = st.session_state["password_history"][-5:]  # Show last 5 records
    for pwd, strength, timestamp in history_data:
        st.write(f"⏰ `{timestamp}` — **{strength}**: `{pwd}`")

    # Clear history button
    if st.button("🗑️ Clear Password History"):
        st.session_state["password_history"] = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("📌 **Built with Danish Haji 🤖 in Python & Streamlit** | 🚀 _Secure your passwords today!_")
