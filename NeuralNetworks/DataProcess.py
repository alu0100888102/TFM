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
    nlogs = len(d)
    npdata = []
    nplabels = []
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
            nplabels.append(0)
        else:
            nplabels.append(1)

    npdata = np.array(npdata, dtype=np.float64)
    nplabels = np.array(nplabels, dtype=np.float32)
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

    nlogs = len(d)
    npdata = []
    nplabels = []
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
            nplabels.append(0)
        else:
            nplabels.append(1)

    npdata = np.array(npdata, dtype=np.float64)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
    print(out)
    return out


def loaddata_split_LSTM(route, fro, to):
    npdata = []
    nplabels = []
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        j = 0
        rerex = []
        for log in d:
            temporal = []
            temporal.append(log["PID"])
            temporal.append(log["TID"])
            temporal.append(log["TS"])
            temporal.append(log["PN"])
            temporal.append(log["OPC"])
            for k in log["PL"]:
                temporal.append(k)
            rerex.append(temporal)
            if j == 99:
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(1)
                j = -1
            j += 1
        #for i in range(len(rerex), 100):
            #temporal = []
            #temporal.append(0)
            #temporal.append(0)
            #temporal.append(0)
            #temporal.append(0)
            #temporal.append(0)
            #for h in range(60):
                #temporal.append(0)
            #rerex.append(temporal)
        #nplabels.append(1)

        #npdata.append(np.array(rerex, dtype=np.float64))


    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        j = 0
        rerex = []
        for log in d:
            temporal = []
            temporal.append(log["PID"])
            temporal.append(log["TID"])
            temporal.append(log["TS"])
            temporal.append(log["PN"])
            temporal.append(log["OPC"])
            for k in log["PL"]:
                temporal.append(k)
            rerex.append(temporal)
            if j == 99:
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(0)
                j = -1
            j += 1
        #for i in range(len(rerex), 100):
        #    temporal = []
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    for h in range(60):
        #        temporal.append(0)
        #    rerex.append(temporal)
        #nplabels.append(0)
        #npdata.append(np.array(rerex, dtype=np.float64))

    npdata = np.array(npdata)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
    print(out)
    return out


def loaddata_hash_LSTM(route, fro, to):
    npdata = []
    nplabels = []
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        j = 0
        rerex = []
        for log in d:
            temporal = []
            temporal.append(log["PID"])
            temporal.append(log["TID"])
            temporal.append(log["TS"])
            temporal.append(log["PN"])
            temporal.append(log["OPC"])
            temporal.append(log["PL"])
            rerex.append(temporal)
            if j == 99:
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(1)
                j = -1
            j += 1
        #for i in range(len(rerex), 100):
        #    temporal = []
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    rerex.append(temporal)
        #nplabels.append(1)

        #npdata.append(np.array(rerex, dtype=np.float64))


    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        j = 0
        rerex = []
        for log in d:
            temporal = []
            temporal.append(log["PID"])
            temporal.append(log["TID"])
            temporal.append(log["TS"])
            temporal.append(log["PN"])
            temporal.append(log["OPC"])
            temporal.append(log["PL"])
            rerex.append(temporal)
            if j == 99:
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(0)
                j = -1
            j += 1
        #for i in range(len(rerex), 100):
        #    temporal = []
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    temporal.append(0)
        #    rerex.append(temporal)
        #nplabels.append(0)
        #npdata.append(np.array(rerex, dtype=np.float64))

    npdata = np.array(npdata)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
    print(out)
    return out
