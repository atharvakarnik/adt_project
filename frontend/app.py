import streamlit as st
import requests

st.title('Employee Timesheet Management System')

username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Login'):
    # Here you would send a request to your Flask/Django API
    # For now, it's just a placeholder
    response = requests.post('http://localhost:5000/login', json={"username": username, "password": password})
    if response.status_code == 200:
        st.success('Logged in successfully.')
        # You can add more Streamlit components based on the user role
    else:
        st.error('Login failed.')