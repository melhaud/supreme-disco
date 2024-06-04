import streamlit as st
import requests

# Define the FastAPI endpoint
url = 'http://backend:8000/' # 'http://localhost:8000/' 'http://127.0.0.1:8000/'

# Make a GET request to the FastAPI app
response = requests.get(url)

# defines an h1 header
st.title("Arrhenius analysis")

# displays a file uploader widget
# TODO limit file extensions to CSV only
data = st.file_uploader("Choose a *.CSV file with your data")

# # displays a button
# if st.button("Get E$_a$"):
#     if data is not None:
#         files = {"file": data.getvalue()}
#         res = requests.post(f"http://backend:8080/{predict}", files=files)
#         pred_path = res.json()
#     #     image = Image.open(pred_path.get("name"))
#     #     st.image(image, width=500)

# Display the response in the Streamlit app
st.write(response.json())