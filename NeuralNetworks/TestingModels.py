import tensorflow as tf
from tensorflow import keras
import DataProcess as dp
import numpy as np


route = "ProcessedLogs\\Splitted\\"

testdata = dp.loaddata_split(route, 1, 5)

print(testdata[0].shape)
print(testdata[1].shape)


model = keras.models.load_model("Models\\LSTMcross3.mdl")
predictions = model.predict(testdata[0])
TP, TN, FP, FN = 0, 0, 0, 0
acc = 0
for i in range(len(testdata[0])):
    pre = 0
    if predictions[i][1] >= 0.5:
        pre = 1
    if  pre == testdata[1][i]:
        acc += 1
        if testdata[1][i] == 1:
            TP +=1
        else:
            TN += 1
    else:
        if testdata [1][i] == 1:
            FN += 1
        else:
            FP += 1
acc = acc/len(testdata[0])
good = 0
bad = 0
for x in testdata[1]:
    if x < 1:
        good += 1
    else:
          bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))
print("ACC: " + str(acc))
print("TP: " + str(TP))
print("TN: " + str(TN))
print("FP: " + str(FP))
print("FN: " + str(FN))

finaltests = dp.loaddata_split_wholefile(route, 1, 25)
print(finaltests[0][0].shape)
TP, TN, FP, FN = 0, 0, 0, 0
results = {}
thold = 0.70
for i in range(50):
    e = np.array(finaltests[0][i])
    predictions = model.predict(e)
    maxgood = 0
    maxbad = 0
    avgbad = 0
    avggood = 0
    count = 0
    acc = 0
    for p in predictions:
        acc += p[1]
        acc = acc / 2
        count += 1
        avggood += p[0]
        avgbad += p[1]
        if p[0] > maxgood:
            maxgood = p[0]
        if p[1] > maxbad:
            maxbad = p[1]
        if acc > thold:
            print("ALERT: " + str(finaltests[1][i]))
            break
    avgbad = avgbad/count
    avggood = avggood/count
    if acc >= thold:
        print("\t" + str(finaltests[1][i]) + " ==> BAD")
        if i < 25:
            TP += 1
        else:
            FP += 1
    else:
        print("\t" + str(finaltests[1][i]) + " ==> GOOD")
        if i >= 25:
            TN += 1
        else:
            FN += 1
    results[avgbad] = finaltests[1][i]
print ("TP: " + str(TP))
print ("TN: " + str(TN))
print ("FP: " + str(FP))
print ("FN: " + str(FN))
r = sorted(results.keys())

for e in r:
    print(str(results[e]) + ": " + str(e))