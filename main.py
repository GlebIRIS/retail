import streamlit as st

# Hardcoded username and password for demonstration purposes
# Replace these with actual user credentials in a production scenario
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def authenticate(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

def main():
    st.title("Login Page")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check login credentials
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            show_form_based_on_credentials(username)
        else:
            st.error("Invalid credentials")

def show_form_based_on_credentials(username):
    # Placeholder for different forms based on user credentials
    st.write(f"Welcome, {username}!")

if __name__ == "__main__":
    main()
