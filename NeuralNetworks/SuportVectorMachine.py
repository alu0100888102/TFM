import sklearn
from sklearn import tree
import DataProcess as dp
import random as rd
from sklearn import svm

fro = 1
to = 25
route = "ProcessedLogs\\Splitted\\"

trainingdata = dp.loaddata_split_tree(route, fro, to)
testdata = [[],[]]
clf = svm.SVC(gamma='scale')


testsize = int(0.3*len(trainingdata[0]))
print(testsize)
for i in range(testsize):
    r = rd.randint(0, len(trainingdata)-1)
    testdata[0].append(trainingdata[0][r])
    testdata[1].append(trainingdata[1][r])
    del(trainingdata[0][r])
    del(trainingdata[1][r])

clf = clf.fit(trainingdata[0], trainingdata[1])
print("YEEE")
testresults = clf.predict(testdata[0])


acc = 0
totalgood = 0
totalbad = 0
TP, TN, FP, FN = 0, 0, 0, 0
for i in range(len(testresults)):
    if testdata[1][i] == 0:
        totalgood += 1
    else:
        totalbad += 1
    if testresults[i] == testdata[1][i]:
        acc += 1
        if testresults[i] == 1:
            TP += 1
        else:
            TN += 1
    else:
        if testdata[1][i] == 1:
            FN += 1
        else:
            FP += 1

acc = acc/len(testresults)

print("Total good:" + str(totalgood))
print("Total bad:" + str(totalbad))
print("TP:" + str(TP))
print("FP:" + str(FP))
print("TN:" + str(TN))
print("FN:" + str(FN))
print("Accuracy: " + str(100*acc) +"%")

finaltests = dp.loaddata_split_wholefile_tree(route, 1, 25)

results = {}
TP, TN, FP, FN = 0, 0, 0, 0
for i in range(50):
    acc = 0
    pred = clf.predict(finaltests[0][i])
    val = 1
    if i >= 25:
        val = 0
    for p in pred:
        acc += p
    acc =  acc/len(pred)
    if acc >= 0.5:
        print("\t" + str(finaltests[1][i]) +": acc = "+str(acc) + " ==> BAD")
        if i < 25:
            TP += 1
        else:
            FP += 1
    else:
        print("\t" + str(finaltests[1][i]) +": acc = "+str(acc) + " ==> GOOD")
        if i > 24:
            TN += 1
        else:
            FN += 1
print ("TP: " + str(TP))
print ("TN: " + str(TN))
print ("FP: " + str(FP))
print ("FN: " + str(FN))