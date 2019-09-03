import re
import json

name = "bad"
numberbot = 1
numbertop = 25

events = {'Process/Start': 0, 'Thread/Start': 1, 'Image/Load': 2, 'DiskIO/Read': 3, 'Image/Unload': 4, 'UdpIp/Send': 5, 'UdpIp/Recv': 6, 'TcpIp/Send': 7, 'TcpIp/Recv': 8, 'Thread/Stop': 9, 'DiskIO/Write': 10, 'Process/Stop': 11}


def getEventNames ():
    eventnames = {}
    counter = 0
    for i in range(numberbot, numbertop):
        e = i + 1
        filename = "good" + str(e) + ".txt"

        f = open("DumpPile\\" + filename, "r")
        logs = []
        for x in f:
            logs.append(json.loads(x))
        for log in logs:
            data = {}
            if "ID" in log:
                t = log["Payload"]["Event"]
            else:
                t = log["Event"]
            if t["@EventName"] not in eventnames:
                eventnames[t["@EventName"]] = counter
                counter += 1

    for i in range(numberbot, numbertop):
        e = i + 1
        filename = "bad" + str(e) + ".txt"

        f = open("DumpPile\\" + filename, "r")
        logs = []
        for x in f:
            logs.append(json.loads(x))
        for log in logs:
            data = {}
            if "ID" in log:
                t = log["Payload"]["Event"]
            else:
                t = log["Event"]
            if t["@EventName"] not in eventnames:
                eventnames[t["@EventName"]] = counter
                counter += 1
    return eventnames

def split(payload):
    temp = str(payload)
    out = []
    for i in range(60):
        r = temp[int(i*9) : int((i+1)*9)]
        for j in range(len(r), 9):
            r += "0"
        out.append(int(r))
    return out

def generate ():
    for i in range(numberbot, numbertop+1):
        pids = {}
        pidc = 1
        tidc = 1
        tids = {}
        timestamp = 0
        e = i
        filename = name + str(e) + ".txt"
        f = open("DumpPile\\"+filename, "r")
        logs = []
        for x in f:
            logs.append(json.loads(x))
        entries = []
        format = '\r\n\s+[0-9a-fA-F]+[:]\s+((?P<a>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h>([0-9a-fA-F]){1,2})\s+){0,1}[|]{0,1}\s*((?P<a2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h2>([0-9a-fA-F]){1,2})\s+)\s*.{1,8}\s*.{0,8}(\r\n\s+$){0,1}'
        ereaser = '\g<a>\g<b>\g<c>\g<d>\g<e>\g<f>\g<g>\g<h>\g<a2>\g<b2>\g<c2>\g<d2>\g<e2>\g<f2>\g<g2>\g<h2>'
        for log in logs:
            data = {}
            if "ID" in log:
                   t = log["Payload"]["Event"]
            else:
               t = log["Event"]
            data["PID"] = int(t["@PID"])
            if data["PID"] not in pids:
                pids[data["PID"]] = pidc
                pidc += 1
            data["PID"] = pids[data["PID"]]
            data["TID"] = int(t["@TID"])
            if data["TID"] not in tids:
                tids[data["TID"]] = tidc
                tidc += 1
            data["TID"] = tids[data["TID"]]
            data["TS"] = int(re.sub("\.", "", re.sub(",", "", t["@TimeStampQPC"])))
            if timestamp == 0:
                timestamp = data["TS"]
            data["TS"] = data["TS"] - timestamp
            data["PN"] = int(t["@ProcessorNumber"])
            data["OPC"] = int(t["@Opcode"])
            data["EN"] = events[t["@EventName"]]
            temp = re.sub(format, ereaser, t["Payload"]["#text"])
            temp = re.sub("[^0-9a-fA-F]", "", temp)
            temp = int(temp, 16)
            data["PL"] = split(temp)

            entries.append(data)

        print(str(e)+": "+ str(entries))
        f = open("ProcessedLogs\\"+filename, "w+")
        f.write(str(entries))
    return 0

def numberofbytes ():
    max = 0
    for i in range(numberbot, numbertop+1):
        e = i
        filename = name + str(e) + ".txt"

        f = open("DumpPile\\"+filename, "r")
        logs = []
        for x in f:
            logs.append(json.loads(x))

        entries = []
        format = '\r\n\s+[0-9a-fA-F]+[:]\s+((?P<a>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h>([0-9a-fA-F]){1,2})\s+){0,1}[|]{0,1}\s*((?P<a2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h2>([0-9a-fA-F]){1,2})\s+)\s*.{1,8}\s*.{0,8}(\r\n\s+$){0,1}'
        ereaser = '\g<a> \g<b> \g<c> \g<d> \g<e> \g<f> \g<g> \g<h> \g<a2> \g<b2> \g<c2> \g<d2> \g<e2> \g<f2> \g<g2> \g<h2> '
        for log in logs:
            data = {}
            if "ID" in log:
                   t = log["Payload"]["Event"]
            else:
                t = log["Event"]
                temp = re.sub(format, ereaser, t["Payload"]["#text"])
                #temp = re.sub("[^0-9a-fA-F]", "", temp)
                temp = re.split("[\n\s\t]+", temp)
                temp = temp[:-1]

                if len(temp) > max:
                    max = len(temp)
                print(len(temp))
    print("MAX: " + str(max))
    return 0

generate()