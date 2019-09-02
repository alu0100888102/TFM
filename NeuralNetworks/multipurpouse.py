import re
import json
import numpy as np

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

e = loaddata("ProcessedLogs\\Splitted\\", 1, 25)
l = sorted(e.keys())

for t in l:
    print(str(t) + ": " + str(e[t]))
