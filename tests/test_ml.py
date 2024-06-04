import pytest
 # TODO resolve for FASTApi
from ml.model import ReactionOrderFitParams, get_model, get_data
from pathlib import Path

DATAPATH = Path(__file__).parent / "../data/synth_data.csv"

@pytest.fixture(scope="function")
def data():
    # Load the data once for each test function
    return get_data()

# Loads model for each test
@pytest.fixture(scope="function")
def model():
    # Load the model once for each test function
    return get_model()

def test_fit(model):
    # data = get_data()
    model_pred = model(DATAPATH)
    print(f"R2 score: {model_pred.r2:.2f}, app. act. energy: {model_pred.coef:.3f} kJ/mol")
    assert isinstance(model_pred, ReactionOrderFitParams)
    