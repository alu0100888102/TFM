import re
import json

name = "good"
numberbot = 23
numbertop = 23

def split(payload):
    temp = str(payload)
    out = []
    for i in range(60):
        r = temp[int(i*9) : int((i+1)*9)]
        for j in range(len(r), 9):
            r += "0"
        out.append(int(r))
    return out


for i in range(numberbot-1, numbertop):
    e = i+1
    filename = name + str(e) + ".txt"

    f = open("DumpPile\\"+filename, "r")
    logs = []
    for x in f:
        logs.append(json.loads(x))

    entries = []
    log = logs[0]
    format = '\r\n\s+[0-9a-fA-F]+[:]\s+((?P<a>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h>([0-9a-fA-F]){1,2})\s+){0,1}[|]{0,1}\s*((?P<a2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<b2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<c2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<d2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<e2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<f2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<g2>([0-9a-fA-F]){1,2})\s+){0,1}((?P<h2>([0-9a-fA-F]){1,2})\s+)\s*.{1,8}\s*.{0,8}(\r\n\s+$){0,1}'
    ereaser = '\g<a>\g<b>\g<c>\g<d>\g<e>\g<f>\g<g>\g<h>\g<a2>\g<b2>\g<c2>\g<d2>\g<e2>\g<f2>\g<g2>\g<h2>'
    for log in logs:
        data = {}
        if "ID" in log:
               t = log["Payload"]["Event"]
        else:
           t = log["Event"]
        data["PID"] = int(t["@PID"])
        data["TID"] = int(t["@TID"])
        data["TS"] = int(re.sub("\.", "", re.sub(",", "", t["@TimeStampQPC"])))
        data["PN"] = int(t["@ProcessorNumber"])
        data["OPC"] = int(t["@Opcode"])
        temp = re.sub(format, ereaser, t["Payload"]["#text"])
        temp = re.sub("[^0-9a-fA-F]", "", temp)
        temp = int(temp, 16)
        data["PL"] = split(temp)

        entries.append(data)

    print(str(e)+": "+ str(entries))
    f = open("ProcessedLogs\\"+filename, "w+")
    f.write(str(entries))

