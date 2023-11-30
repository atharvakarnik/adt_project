import streamlit as st

# Define a function for user authentication (mockup for now)
def authenticate_user(username, password):
    # Placeholder for actual authentication logic
    # In real app, you would check against a database or authentication service
    if username == "admin" and password == "password123":
        return True
    return False

# Basic layout
st.title("Employee Timesheet Management System")

# Login form
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Login")

    if submit_button:
        if authenticate_user(username, password):
            st.success("Login Successful!")
            # Redirect or show the dashboard
        else:
            st.error("Incorrect Username or Password")