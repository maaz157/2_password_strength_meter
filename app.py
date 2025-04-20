import re
import streamlit as st
import random
import string
import streamlit.components.v1 as components

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ Include at least one uppercase letter.")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ Include at least one lowercase letter.")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❌ Include at least one digit (0-9).")

    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    common_words = ["password", "123456", "qwerty", "admin", "letmein"]
    if any(word in password.lower() for word in common_words):
        feedback.append("⚠️ Avoid using common words or sequences in your password.")
    
    if re.search(r'(.)\1{2,}', password):
        feedback.append("⚠️ Avoid using consecutive repeated characters.")
  
    if re.search(r'123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz', password.lower()):
        feedback.append("⚠️ Avoid using sequential characters (e.g., '1234', 'abcd').")
    
    if score >= 4 and len(set(password)) >= 6:
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
    
    return strength, feedback

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")
    st.title("🔐 Password Strength Meter")
    st.write("Enter a password to check its strength and get suggestions for improvement.")
    
    with st.container():
        password = st.text_input("Enter a password:", type="password")
        col1, col2 = st.columns(2)
        with col1:
            check_btn = st.button("Check Strength")
        with col2:
            generate_btn = st.button("Generate Strong Password")
    
    if check_btn:
        strength, feedback = check_password_strength(password)
        color = {"Weak": "red", "Moderate": "orange", "Strong": "green"}.get(strength, "black")
        st.markdown(f"### Password Strength: <span style='color:{color}; font-weight:bold'>{strength}</span>", unsafe_allow_html=True)
        
        st.progress({"Weak": 0.33, "Moderate": 0.66, "Strong": 1.0}[strength])
        
        if feedback:
            with st.expander("Suggestions to improve your password"):
                for tip in feedback:
                    st.write(tip)
        else:
            st.success("🎉 Great job! Your password is strong.")
    
    if generate_btn:
        strong_password = generate_strong_password()
        st.text_input("Suggested Strong Password:", strong_password, key="generated_password", disabled=True)
        # Add copy to clipboard button using JS
        copy_button_html = f"""
        <input type="text" value="{strong_password}" id="passwordInput" style="opacity:0; position:absolute; left:-9999px;">
        <button onclick="copyPassword()" style="background-color:#4CAF50; color:white; border:none; padding:8px 16px; border-radius:5px; font-weight:bold; cursor:pointer;">
            Copy Password to Clipboard
        </button>
        <script>
        function copyPassword() {{
            var copyText = document.getElementById("passwordInput");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Password copied to clipboard!");
        }}
        </script>
        """
        components.html(copy_button_html, height=50)
    
    # Custom CSS for buttons
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            height: 3em;
            width: 100%;
            border-radius: 10px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        div.stButton > button:hover {
            background-color: #45a049;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    st.markdown("🔹 **Tip:** Use a combination of uppercase, lowercase, numbers, and special characters for a strong password.")
    st.markdown("🔹 **Note:** Avoid common words, repeated or sequential characters for better security.")
    st.markdown("© 2024 Password Strength Meter App")

if __name__ == "__main__":
    main()
