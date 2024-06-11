import streamlit as st
from shap import TreeExplainer
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()


df = conn.read(
    worksheet="Sheet1",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

def calculate_shap(model, X_train, X_test):
    explainer = TreeExplainer(model)
    shap_values_train = explainer.shap_values(X_train)
    shap_values_test = explainer.shap_values(X_test)
    return explainer, shap_values_train, shap_values_test
# Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")


