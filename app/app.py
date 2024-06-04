from fastapi import FastAPI
from pydantic import BaseModel

 # TODO resolve for FASTApi
from ml.model import ReactionOrderFitParams, get_model, get_data
from pandas import DataFrame


model = None
app = FastAPI(
    title="Arrhenius analysis",
    description="""
    Apparent activation energy computation from 
    yield concentration and temperature data provided in *.CSV
    """,
    version="0.0.1"
)



# class ReactionOrderFitParams(BaseModel):
#     """
#     Dataclass for apparent activation energy prediction.
#     """
#     r2 : float
#     coef : float
#     intercept : float

# app root
@app.post("/home")
def index():
    return {"text": "Apparent activation energy prediction"}

# app startup
@app.on_event("startup")
def startup_event():
    global model # TODO change datafile path fixed in model.py
    model = get_model()

# coefficient of fit
@app.get("/predict")
def get_params():
    # TODO unfix datafile path
    x,y = get_data()
    model = model(x,y) 

    fit_params = ReactionOrderFitParams(
        r2=model.score(x, y),
        coef=model.coef_,
        intercept=model.intercept_,
    )

    return fit_params

# @app.post("/prediction")
# def get_prediction():
#     return 1