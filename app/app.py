from fastapi import FastAPI
from pydantic import BaseModel
from ml.model import load_model

from pandas import DataFrame

model = None
app = FastAPI()

class ReactionOrderFitParams(BaseModel):
    """
    Dataclass for apparent activation energy prediction.
    """
    r2 : float
    coef : float
    intercept : float

# app root
@app.get("/")
def index():
    return {"text": "Apparent activation energy prediction"}

# app startup
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

# coefficient of fit
@app.get("/predict")
def predict_sentiment(data: DataFrame):

    model = model(data) 

    fit_params = ReactionOrderFitParams(
        r2=model.score(data),
        coef=model.coef_,
        intercept=model.intercept_,
    )

    return fit_params