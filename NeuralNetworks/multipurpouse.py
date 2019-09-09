import re
import json
import DataProcess as dp
import numpy as np
import tensorflow as tf
from tensorflow import keras

def loaddata(route, fro, to):
    d = []
    l = []
    for e in range(fro-1, to):
        filename1 = "bad" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        filename2 = "good" + str(e + 1) + ".txt"
        f = open(route+filename2, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)
        for log in t:
            d.append(log)
            l.append(0)
    out = {}
    for i in range(len(d)):
        log = d[i]
        key = log["PN"]
        name = l[i]
        if key in out:
            if name not in out[key]:
                out[key].append(name)
        else:
            out[key] = []
            out[key].append(name)

    return out

#print(keras.metrics.FalseNegatives())
#e = loaddata("ProcessedLogs\\Splitted\\", 1, 25)
#l = sorted(e.keys())

#for t in l:
    #print(str(t) + ": " + str(e[t]))

fro = 1
to = 25
route = "ProcessedLogs\\Splitted\\"

trainingdata = dp.loaddata_split(route, fro, to)

good = 0
bad = 0
for x in trainingdata[1]:
    if x < 1:
        good += 1
    else:
        bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))

