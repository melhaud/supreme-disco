import streamlit as st
import requests

# Define the FastAPI endpoint
url = 'http://127.0.0.1:8000/' # 'http://localhost:8000/'

# Make a GET request to the FastAPI app
response = requests.get(url)

# Display the response in the Streamlit app
st.write(response.json())