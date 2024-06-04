import streamlit as st
import requests
import json
from io import StringIO

from ml.model import (get_model,
                      get_fit_params,
                      get_data_from_text,
                      DATAPATH) # TODO add flexibility in choosing default or custom data

from file_utils import (
    upload_file_or_reject,
    InvalidFileExtension,
    upload_folder,
    output_folder,
)

# Define the FastAPI endpoint
url = "https://supreme-disco.streamlit.app/home"
# url = '/' # "http://fastapi:8000/app" 'http://localhost:8000/' 'http://127.0.0.1:8000/' 'http://backend:8000/'

# Make a GET request to the FastAPI app
response = requests.get(url)

# defines an h1 header
st.title("Arrhenius analysis")

# displays a file uploader widget
# TODO limit file extensions to CSV only
data_txt = st.file_uploader("Choose a *.CSV file with your data",
                        type=['csv'], # 'xlsx',
                        accept_multiple_files=False)

# # Check extension of an uploaded file
# try:
#     upload_file_or_reject(data_txt, upload_folder)
# except InvalidFileExtension as e:
#     st.write(e)

# uploaded_data_path = None
if data_txt is not None:
    stringio = StringIO(data_txt.getvalue().decode("utf-8"))
    # To read file as string:
    string_data = stringio.read()
    st.code(string_data)
    data = get_data_from_text(string_data)

if data:
    model = get_model(data)

if model and data:
    st.button(label="Run computation", on_click=get_fit_params, args=[data, model])


# # displays a button
# if st.button("Get E$_a$"):
#     if data is not None:
#         files = {"file": data.getvalue()}
#         res = requests.post(f"http://backend:8080/{predict}", files=files)
#         pred_path = res.json()
#     #     image = Image.open(pred_path.get("name"))
#     #     st.image(image, width=500)

# Display the response in the Streamlit app
# st.write(response.json())
