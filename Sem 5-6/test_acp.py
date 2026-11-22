import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from functii import *
from grafice import*

data_set=pd.read_csv("data_in/I2014.csv", index_col="DenLocalitate")
# print(data_set)
# verific daca am val lipsa
nan_replace_df(data_set)

# sar primele 2 col
var_obs=list(data_set)[2:]
x=data_set[var_obs].values










