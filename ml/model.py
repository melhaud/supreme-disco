from dataclasses import dataclass
from pandas import DataFrame, read_csv
from numpy import log
from sklearn.linear_model import LinearRegression

import yaml
from pathlib import Path

allowed_x = ["T", "rec T K"]
allowed_y = ["yield", "log_yield"]

# load config and data files
CONFIGPATH = Path(__file__).parent / "config_act_energy.yaml"

with open(CONFIGPATH, "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

DATAPATH = Path(__file__).parent / "../data/synth_data.csv"

@dataclass
class ReactionOrderFitParams:
    """
    Dataclass for apparent activation energy prediction.
    """
    r2 : float
    coef : float
    intercept : float
    # label: str
    # score: float

def get_data(data_path: str = DATAPATH):
    data = read_csv(data_path, header=0)
    if (config["x"] not in allowed_x) or (config["y"] not in allowed_y):
        raise ValueError("Please check the column names")

    if config["x"] == "T":
        data["rec T K"] = -1000 / (data[config["x"]] + 273.15) / 8.314
        return data["rec T K"], data[config["y"]]
    
    if config["y"] == "yield":
        data["log_yield"] = data[config["y"]].apply(log)
        return data[config["x"]], data["log_yield"]

    return data[config["x"]], data[config["y"]]

def get_model():

    def model(data_path: str) -> ReactionOrderFitParams:
        data = get_data(data_path)
        x,y = data[0].values.reshape(-1, 1), data[1].values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(x,y)
    
        return ReactionOrderFitParams(
            r2=model.score(x,y),
            coef=float(model.coef_[0]),
            intercept=model.intercept_
        )
    
    return model
