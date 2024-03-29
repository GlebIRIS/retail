import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import subprocess
import base64
# Install PyGithub
subprocess.call(["pip", "install", "PyGithub"])
USERNAME = "GlebIRIS"
REPO_NAME = "retail"
ACCESS_TOKEN = "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"

def main():
    st.title("Survey App")

    # Initialize session_state to keep track of pages
    if 'page' not in st.session_state:
        st.session_state.page = 1
        st.session_state.survey_responses = {}
        st.session_state.csv_exists = False  # Initialize csv_exists

    if st.session_state.page == 1:
        login_page()
    elif st.session_state.page == 2:
        survey_page()
    elif st.session_state.page == 3:
        additional_survey_page()

def login_page():
    st.title("Login Page")

    # Questions
    username = st.text_input("Username (Answer to Question 1):")
    password = st.text_input("Password (Answer to Question 2):", type="password")

    if st.button("Submit Answers"):
        # Validate login
        if validate_login(username, password):
            st.session_state.page += 1
        else:
            st.error("Incorrect answers to the first two questions. Please try again.")

def survey_page():
    st.title("Survey Questions")

    # Additional Questions
    question3 = st.text_input("Question 3:")

    if st.button("Next"):
        # Save answers to survey_responses
        st.session_state.survey_responses['Question 3'] = question3

        st.session_state.page += 1

def additional_survey_page():
    st.title("Additional Survey Questions")

    # Additional Questions
    question4 = st.text_input("Question 4:")
    question5 = st.text_input("Question 5:")
    question6 = st.text_input("Question 6:")

    if st.button("Submit Survey"):
        # Save answers to survey_responses
        st.session_state.survey_responses['Question 4'] = question4
        st.session_state.survey_responses['Question 5'] = question5
        st.session_state.survey_responses['Question 6'] = question6

        # Generate unique response ID
        response_id = generate_response_id(st.session_state.survey_responses['Question 3'])

        # Save survey_responses to CSV file
        save_to_csv(response_id, st.session_state.survey_responses)
        st.success("Survey submitted successfully!")
        commit_and_push_to_github()

def generate_response_id(question3_answer):
    # Generate unique response ID based on the answer to Question 3 and the date
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{question3_answer}_{date_str}"

def validate_login(username, password):
    # Customize the validation logic based on your requirements
    return username.lower() == "admin" and password.lower() == "admin"

def save_to_csv(response_id, data):
    # Rearrange the data and create a DataFrame
    response_data = {'Response ID': [], 'Question': [], 'Answer': []}

    for question, answer in data.items():
        if question.lower() not in ['question 1', 'question 2']:
            response_data['Response ID'].append(response_id)
            response_data['Question'].append(question)
            response_data['Answer'].append(answer if answer else 'Empty')

    df = pd.DataFrame(response_data)

    # Save DataFrame to CSV file
    df.to_csv('survey_responses.csv', mode='a', index=False, header=not st.session_state.csv_exists)
    st.session_state.csv_exists = True

    # Print for debugging
    print("Saved to CSV:", response_id, data)

def commit_and_push_to_github():
    # GitHub repository details
    repo_url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/survey_responses.csv"
    commit_url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main"

    # Read the contents of the local CSV file
    with open('survey_responses.csv', 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Get the existing file on GitHub to obtain its SHA
    response = requests.get(repo_url, auth=HTTPBasicAuth(USERNAME, ACCESS_TOKEN))
    response_data = response.json()

    if response.status_code == 200:
        sha = response_data['sha']
    else:
        sha = None

    # Update the file on GitHub
    commit_message = "Update survey responses"
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}

    if sha is not None:
        update_data = {
            "message": commit_message,
            "content": content,
            "sha": sha,
            "branch": "main"
        }
        response = requests.put(repo_url, headers=headers, json=update_data)
    else:
        create_data = {
            "message": commit_message,
            "content": content,
            "branch": "main"
        }
        response = requests.put(repo_url, headers=headers, json=create_data)

    if response.status_code == 200 or response.status_code == 201:
        print("Committed and pushed to GitHub:", commit_message)
    else:
        print("Error committing and pushing to GitHub:", response.text)

    # Print for debugging
    print("Committed and pushed to GitHub:", commit_message)

if __name__ == "__main__":
    main()
