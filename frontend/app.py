import streamlit as st
import requests

def login_user(username, password):
    response = requests.post('http://localhost:5000/login', json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    return None

def show_employee_dashboard():
    st.write("Employee Dashboard")
    if st.button('Clock In'):
        # Logic for clocking in
        st.write("Clocked In Successfully")

def show_manager_dashboard():
    st.write("Manager Dashboard")
    if st.button('Add Employee'):
        st.session_state['current_page'] = 'add_employee'

def add_employee_page():
    st.write("Add Employee")
    # Add your form and logic here for adding an employee

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'

# Title
st.title('Employee Timesheet Management System')

# Page logic
if st.session_state['current_page'] == 'login':
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        user_info = login_user(username, password)
        if user_info:
            st.success('Logged in successfully.')
            if user_info.get("is_manager"):
                st.session_state['current_page'] = 'manager_dashboard'
            else:
                st.session_state['current_page'] = 'employee_dashboard'
        else:
            st.error('Login failed.')

elif st.session_state['current_page'] == 'employee_dashboard':
    show_employee_dashboard()

elif st.session_state['current_page'] == 'manager_dashboard':
    show_manager_dashboard()

elif st.session_state['current_page'] == 'add_employee':
    add_employee_page()
