import pandas as pd
import json


def read_data(file):
    with open(file, "r") as f:
        data = json.load(f)
    