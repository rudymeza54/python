import os
import pandas as pd
import json
import zipfile
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import gzip

path = (r"C:\Users\rudym\OneDrive\Desktop\VS Code\python\data")



dir = os.listdir(path)[1]

for i in dir:
    full_path = os.path.join(path, i)
    data = gzip.open(full_path, "rb")
    data = pd.read_csv(data)


states_df = pd.read_csv(os.path.join(path, states))

states_df["code"] = states_df["code"].astype("int")

data.head()

states_df