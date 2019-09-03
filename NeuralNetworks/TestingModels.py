import tensorflow as tf
from tensorflow import keras
import DataProcess as dp
import numpy as np

fro = 1
to = 20
route = "ProcessedLogs\\Splitted\\"

#testdata = dp.loaddata_split_LSTM(route, 21, 25, 100)

#print(testdata[0].shape)
#print(testdata[1].shape)


model = keras.models.load_model("Models\\LSTMSplittedTemporal_NewGen.mdl")

#loss, accu = model.evaluate(testdata[0], testdata[1])
#print("Test samples accuracy:", accu)
#print("Test loss accuracy:", loss)

#good = 0
#bad = 0
#for x in testdata[1]:
#    if x < 1:
#        good += 1
#    else:
#        bad += 1

#print("Good: " + str(good) + ", Bad: " + str(bad))

finaltests = dp.loaddata_hash_LSTM_wholefile(route, 1, 25, 25)
TP, TN, FP, FN = 0, 0, 0, 0
results = {}
for i in range(50):
    e = np.array(finaltests[0][i])
    predictions = model.predict(e)
    maxgood = 0
    maxbad = 0
    for p in predictions:
        if p[0] > maxgood:
            maxgood = p[0]
        if p[1] > maxbad:
            maxbad = p[1]
    print(str(finaltests[1][i]) + ":")
    print("\tGOOD: " + str(maxgood))
    print("\tBAD: " + str(maxbad))
    if maxbad > 0.75:
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
    results[maxbad] = finaltests[1][i]
print ("TP: " + str(TP))
print ("TN: " + str(TN))
print ("FP: " + str(FP))
print ("FN: " + str(FN))
r = sorted(results.keys())

for e in r:
    print(str(results[e]) + ": " + str(e))