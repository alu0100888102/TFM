import tensorflow as tf
from tensorflow import keras
import DataProcess as dp
import random as rd
import math
import numpy as np

fro = 6
to = 21
route = "ProcessedLogs\\Splitted\\"
nfolds = 10

trainingdata = dp.loaddata_split_LSTM_moving_crossval(route, fro, to, 50)
rd.shuffle(trainingdata)
print(len(trainingdata))
foldsize = int(len(trainingdata) / nfolds)

model = keras.Sequential([
    keras.layers.LSTM(16),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer=keras.optimizers.RMSprop(lr=0.05),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

testresults = [[], []]
for i in range(nfolds):
    print("Fold " + str(i+1) + " ====================================================================================================")
    start = i * foldsize
    end = (i+1) * foldsize
    training = [[], []]
    test = [[], []]
    for j in range(len(trainingdata)):
        if (j >= start and j < end):
            test[0].append(trainingdata[j][0])
            test[1].append(trainingdata[j][1])
        else:
            training[0].append(trainingdata[j][0])
            training[1].append(trainingdata[j][1])
    test[0] = np.array(test[0])
    test[1] = np.array(test[1], dtype=np.float32)
    training[0] = np.array(training[0])
    training[1] = np.array(training[1], dtype=np.float32)

    model.fit(training[0], training[1], epochs=50)
    loss, accu = model.evaluate(test[0], test[1])
    testresults[0].append(loss)
    testresults[1].append(accu)

meanaccu = 0
meanloss = 0
for k in range(nfolds):
    print("Test" + str(k) + "==> loss:" + str(testresults[0][k]) + "accuracy:" + str(testresults[1][k]))
    meanloss += testresults[0][k]
    meanaccu += testresults[1][k]
meanloss = meanloss/nfolds
meanaccu = meanaccu/nfolds
print("Test mean ==> loss:" + str(meanloss) + " accuracy:" + str(meanaccu))
model.save("Models\\LSTMcrosswindow.mdl")