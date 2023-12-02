import streamlit as st
import requests

# Base URL for backend API
BACKEND_API = 'http://localhost:5000'

def login_user(username, password):
    response = requests.post(f'{BACKEND_API}/login', json={"username": username, "password": password})
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
    with st.form("add_employee_form"):
        emp_name = st.text_input("Employee Name", key='emp_name')
        dept_name = st.text_input("Department Name", key='dept_name')
        location_name = st.text_input("Location Name", key='location_name')
        username = st.text_input("Username", key='username')
        password = st.text_input("Password", type="password", key='password')
        is_manager = st.checkbox("Is Manager?", key='is_manager')
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            response = requests.post(f'{BACKEND_API}/add_employee', json={
                "emp_name": emp_name,
                "dept_name": dept_name,
                "location_name": location_name,
                "username": username,
                "password": password,
                "is_manager": is_manager
            })

            if response.status_code == 201:
                st.success("Employee added successfully.")
                st.session_state['current_page'] = 'manager_dashboard'
            else:
                st.error("Failed to add employee. Please try again.")

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
