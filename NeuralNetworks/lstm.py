import tensorflow as tf
import pandas as pd
import numpy as np
import json


f = open("DumpPile\\bad1.txt", "r")
log = []
for x in f:
    print(x)
    t = json.loads(x)

