import re
import json
import numpy as np


def loaddata_hash(route, fro, to):
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
    print(d)
    print(l)

    nlogs = len(d)
    npdata = []
    nplabels = [[],[]]
    for i in range(nlogs):
        npdata.append([
            d[i]["PID"],
            d[i]["TID"],
            d[i]["TS"],
            d[i]["PN"],
            d[i]["OPC"],
            d[i]["PL"]
        ])
        if l[i] == 0:
            nplabels.append([1, 0])
        else:
            nplabels.append([0, 1])

    npdata = np.array(npdata, dtype=np.float64)
    nplabels = np.array(l, dtype=np.float32)
    out =[npdata, nplabels]
    return out

def loaddata_split(route, fro, to):
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
    print(d)
    print(l)

    nlogs = len(d)
    npdata = []
    nplabels = [[],[]]
    for i in range(nlogs):
        temporal = []
        temporal.append(d[i]["PID"])
        temporal.append(d[i]["TID"])
        temporal.append(d[i]["TS"])
        temporal.append(d[i]["PN"])
        temporal.append(d[i]["OPC"])
        for k in d[i]["PL"]:
            temporal.append(k)
        npdata.append(temporal)
        if l[i] == 0:
            nplabels.append([1, 0])
        else:
            nplabels.append([0, 1])

    npdata = np.array(npdata, dtype=np.float64)
    nplabels = np.array(l, dtype=np.float32)
    out =[npdata, nplabels]
    return out
