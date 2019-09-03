import re
import json
import numpy as np
import random as rd

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


def loaddata_split_LSTM(route, fro, to, size):
    npdata = []
    nplabels = []
    size = size-1
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        print(filename1)
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
            #temporal.append(log["PID"])
            #temporal.append(log["TID"])
            #temporal.append(log["TS"])
            #temporal.append(log["PN"])
            #temporal.append(log["OPC"])
            temporal.append(log["EN"])
            for k in log["PL"]:
                temporal.append(k)
            rerex.append(temporal)
            if j == size:
                print (rerex)
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(1)
                j = -1
            j += 1
    print(len(npdata))

    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        print(filename1)
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(0)

        j = 0
        rerex = []
        for log in d:
            temporal = []
            #temporal.append(log["PID"])
            #temporal.append(log["TID"])
            #temporal.append(log["TS"])
            #temporal.append(log["PN"])
            #temporal.append(log["OPC"])
            temporal.append(log["EN"])
            for k in log["PL"]:
                temporal.append(k)
            rerex.append(temporal)
            if j == size:
                npdata.append(np.array(rerex, dtype=np.float64))
                rerex = []
                nplabels.append(0)
                j = -1
            j += 1

    npdata = np.array(npdata)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
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
            #temporal.append(log["PID"])
            #temporal.append(log["TID"])
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

    npdata = np.array(npdata)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
    print(out)
    return out


def loaddata_split_LSTM_moving(route, fro, to, size):
    npdata = []
    nplabels = []
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        print(filename1)
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        PIDlist = dict()
        for log in t:
            if log["PID"] not in PIDlist:
                s = len(PIDlist)
                PIDlist[log["PID"]] = s
                d.append([])
                l.append([])

            pos = PIDlist[log["PID"]]
            d[pos].append(log)
            l[pos].append(1)

        for process in d:
            if len(process) >= size:
                bot = 0
                top = size
                while len(process) > top:
                    rerex = []
                    for y in range(bot, top):
                        temporal = [process[y]["EN"]]
                        for k in process[y]["PL"]:
                            temporal.append(k)
                        rerex.append(temporal)
                    npdata.append(np.array(rerex, dtype=np.float64))
                    nplabels.append(1)
                    bot += 1
                    top += 1


    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        PIDlist = dict()
        for log in t:
            if log["PID"] not in PIDlist:
                s = len(PIDlist)
                PIDlist[log["PID"]] = s
                d.append([])
                l.append([])

            pos = PIDlist[log["PID"]]
            d[pos].append(log)
            l[pos].append(1)


        for process in d:
            if len(process) >= size:
                bot = 0
                top = size
                while len(process) > top:
                    rerex = []
                    for y in range(bot, top):
                        temporal = [process[y]["EN"]]
                        for k in process[y]["PL"]:
                            temporal.append(k)
                        rerex.append(temporal)
                    npdata.append(np.array(rerex, dtype=np.float64))
                    nplabels.append(0)
                    bot += 1
                    top += 1

    nplabels = np.array(nplabels, dtype=np.float32)
    out = [np.array(npdata), nplabels]
    #print(out)
    return out

def loaddata_split_LSTM_moving_halfandhalf(route, fro, to, size):
    npdata = []
    nplabels = []
    count = 1866 #2384
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        print(filename1)
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        PIDlist = dict()
        for log in t:
            if log["PID"] not in PIDlist:
                s = len(PIDlist)
                PIDlist[log["PID"]] = s
                d.append([])
                l.append([])

            pos = PIDlist[log["PID"]]
            d[pos].append(log)
            l[pos].append(1)

        for process in d:
            if len(process) >= size:
                bot = 0
                top = size
                while len(process) > top:
                    rerex = []
                    for y in range(bot, top):
                        temporal = [process[y]["EN"]]
                        for k in process[y]["PL"]:
                            temporal.append(k)
                        rerex.append(temporal)
                    if count > 0:
                        npdata.append(np.array(rerex, dtype=np.float64))
                        nplabels.append(1)
                        count -= 1
                    bot += 1
                    top += 1



    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        print(filename1)
        f = open(route+filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        PIDlist = dict()
        for log in t:
            if log["PID"] not in PIDlist:
                s = len(PIDlist)
                PIDlist[log["PID"]] = s
                d.append([])
                l.append([])

            pos = PIDlist[log["PID"]]
            d[pos].append(log)
            l[pos].append(1)


        for process in d:
            if len(process) >= size:
                bot = 0
                top = size
                while len(process) > top:
                    rerex = []
                    for y in range(bot, top):
                        temporal = [process[y]["EN"]]
                        for k in process[y]["PL"]:
                            temporal.append(k)
                        rerex.append(temporal)
                    npdata.append(np.array(rerex, dtype=np.float64))
                    nplabels.append(0)
                    bot += 1
                    top += 1

    nplabels = np.array(nplabels, dtype=np.float32)
    out = [np.array(npdata), nplabels]
    #print(out)
    return out


def loaddata_split_LSTM_halfandhalf(route, fro, to):
    npdata = []
    nplabels = []
    tre = 28
    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "bad" + str(e+1) + ".txt"
        print(filename1)
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
            #temporal.append(log["PID"])
            #temporal.append(log["TID"])
            #temporal.append(log["TS"])
            #temporal.append(log["PN"])
            temporal.append(log["OPC"])
            for k in log["PL"]:
                temporal.append(k)
            rerex.append(temporal)
            if j == 99:
                if tre > 0:
                    npdata.append(np.array(rerex, dtype=np.float64))
                    tre -= 1
                    nplabels.append(1)
                rerex = []
                j = -1
            j += 1
    print(len(npdata))

    for e in range(fro-1, to):
        d = []
        l = []
        filename1 = "good" + str(e+1) + ".txt"
        print(filename1)
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
            #temporal.append(log["PID"])
            #temporal.append(log["TID"])
            #temporal.append(log["TS"])
            #temporal.append(log["PN"])
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
    print(len(npdata))

    npdata = np.array(npdata)
    nplabels = np.array(nplabels, dtype=np.float32)
    out =[npdata, nplabels]
    return out

def loaddata_hash_LSTM_wholefile(route, fro, to, size):
    npdata = []
    nplabels = []
    size = size-1
    for e in range(fro - 1, to):
        d = []
        l = []
        filename1 = "bad" + str(e + 1) + ".txt"
        f = open(route + filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(1)

        j = 0
        rerex = []
        frog = []
        for log in d:
            temporal = []
            # temporal.append(log["PID"])
            # temporal.append(log["TID"])
            # temporal.append(log["TS"])
            # temporal.append(log["PN"])
            # temporal.append(log["OPC"])
            temporal.append(log["EN"])
            for k in log["PL"]:
                temporal.append(k)
            frog.append(temporal)
            if j == size:
                rerex.append(np.array(frog, dtype=np.float64))
                frog = []
                j = -1
            j += 1
        npdata.append(np.array(rerex))
        nplabels.append(filename1)

    for e in range(fro - 1, to):
        d = []
        l = []
        filename1 = "good" + str(e + 1) + ".txt"
        f = open(route + filename1, "r")
        x = f.read()
        x = re.sub("\'", "\"", x)
        t = json.loads(x)

        for log in t:
            d.append(log)
            l.append(0)
        rerex = []
        j = 0
        frog = []
        for log in d:
            temporal = []
            # temporal.append(log["PID"])
            # temporal.append(log["TID"])
            # temporal.append(log["TS"])
            # temporal.append(log["PN"])
            # temporal.append(log["OPC"])
            temporal.append(log["EN"])
            for k in log["PL"]:
                temporal.append(k)
            frog.append(temporal)
            if j == size:
                rerex.append(np.array(frog, dtype=np.float64))
                frog = []
                j = -1
            j += 1
        npdata.append(np.array(rerex))
        nplabels.append(filename1)

    out = [npdata, nplabels]
    return out