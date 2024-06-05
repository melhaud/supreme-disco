from dataclasses import dataclass
from typing import Tuple
from io import StringIO
from pandas import DataFrame, read_csv
from numpy import log, ndarray
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

def get_data_from_text(data_text):
    data = read_csv(StringIO(data_text), sep=",")
    # data = DataFrame.from_dict(data_text)
    if (config["x"] not in allowed_x) or (config["y"] not in allowed_y):
        raise ValueError("Please check the column names")

    if config["x"] == "T":
        data["rec T K"] = -1000 / (data[config["x"]] + 273.15) / 8.314
        return data["rec T K"].values.reshape(-1,1), \
            data[config["y"]].values.reshape(-1,1)
    
    if config["y"] == "yield":
        data["log_yield"] = data[config["y"]].apply(log)
        return data[config["x"]].values.reshape(-1,1),\
            data["log_yield"].values.reshape(-1,1)

    return data[config["x"]].values.reshape(-1,1), \
            data[config["y"]].values.reshape(-1,1)

# def get_data(data_path: str = DATAPATH) -> Tuple[ndarray,ndarray]:
    data = read_csv(data_path, header=0)
    if (config["x"] not in allowed_x) or (config["y"] not in allowed_y):
        raise ValueError("Please check the column names")

    if config["x"] == "T":
        data["rec T K"] = -1000 / (data[config["x"]] + 273.15) / 8.314
        return data["rec T K"].values.reshape(-1,1), \
            data[config["y"]].values.reshape(-1,1),
    
    if config["y"] == "yield":
        data["log_yield"] = data[config["y"]].apply(log)
        return data[config["x"]].values.reshape(-1,1),\
            data["log_yield"].values.reshape(-1,1),

    return data[config["x"]].values.reshape(-1,1), \
            data[config["y"]].values.reshape(-1,1)

def get_model(data: Tuple[DataFrame,DataFrame]):
    if isinstance(data, Tuple):
        x,y = data
        model = LinearRegression()
        model.fit(x.reshape(-1,1),\
                    y.reshape(-1,1))

        return model
    else:
        raise ValueError(f"Data seem not to contain necessary columns. Type: {type(data)}")

def get_fit_params(data, model):
    x,y = data
    return f"R2 score: {model.score(x,y):.3f}, \
            activation energy: {float(model.coef_):.3f}, \
            preexponent: {float(model.intercept_):.3f}"

