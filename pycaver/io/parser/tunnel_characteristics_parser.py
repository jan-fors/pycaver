import os
import pandas as pd

def parse_tunnel_characteristics(input_path : str) -> dict:
    """
    Parse the data from tunnel characteristics file
    :input: path to the tunnel_characteristics.csv
    :output: the tunnel characterstics
    """
    if not os.path.exists(input_path):
        print(f"Input Path for tunnel characteristics: {input_path} does not exist.")
        return {}
    else:
        df = pd.read_csv(input_path)
        return df.to_dict()

def parse_tunnel_characteristics_summary(input_path : str) -> dict:
    """
    Parse the data from tunnel characteristics file and return the summary
    :input: path to the tunnel_characteristics.csv
    :output: the tunnel characterstics summary
    """
    data = parse_tunnel_characteristics(input_path)
    res = {}

    # min, max and avg curvature
    curvature = []
    for n in data[" Curvature"].keys():
        curvature.append(float(data[" Curvature"][n]))

    res["min_curvature"] = min(curvature)
    res["max_curvature"] = max(curvature)
    res["avg_curvature"] = sum(curvature) / len(curvature)

    # min, max and avg length
    length = []
    for n in data[" Length"].keys():
        length.append(float(data[" Length"][n]))

    res["min_length"] = min(length)
    res["max_length"] = max(length)
    res["avg_length"] = sum(length) / len(length)

    return res