import tensorflow as tf
from tensorflow import keras
import random as rd
import re
import json
import numpy as np

def loaddata():
    d = []
    l = []
    for e in range(10):
        filename1 = "bad" + str(e+1) + ".txt"
        filename2 = "good" + str(e+1) + ".txt"
        f = open("ProcessedLogs\\"+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)
        for log in t:
            d.append(log)
            l.append(1)
        f = open("ProcessedLogs\\"+filename2, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)
        for log in t:
            d.append(log)
            l.append(0)
    print(d)
    print(l)

    nlogs = len(d)
    npdata = [[],[],[],[],[],[]]
    nplabels = [[],[]]
    for i in range(nlogs):
        npdata[0].append(d[i]["PID"])
        npdata[1].append(d[i]["TID"])
        npdata[2].append(d[i]["TS"])
        npdata[3].append(d[i]["PN"])
        npdata[4].append(d[i]["OPC"])
        npdata[5].append(d[i]["PL"])
        if l[i] == 0:
            nplabels[0].append(1)
            nplabels[1].append(0)
        else:
            nplabels[0].append(0)
            nplabels[1].append(1)

    npdata = np.array(npdata, dtype=np.float64)
    nplabels = np.array(l, dtype=np.float32)
    out =[npdata, nplabels]
    return out

def getrandombatch(size, data):
    if len(data) <= size:
        return data
    out = []
    for i in range(size):
        r = rd.randint(0, len(data)-1)
        out.append(data[r])
        del data[r]
    return out

trainingdata = loaddata()
print(trainingdata)

model = keras.Sequential([
    keras.layers.Dense(6),
    keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(trainingdata[0], trainingdata[1], steps_per_epoch=1000)