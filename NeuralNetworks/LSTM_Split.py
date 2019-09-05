import tensorflow as tf
from tensorflow import keras
import DataProcess as dp
import random as rd
import numpy as np

fro = 1
to = 2
route = "ProcessedLogs/Splitted/"

trainingdata = dp.loaddata_split_LSTM(route, fro, to, 50)
testdata = dp.loaddata_split_LSTM(route, 3, 4, 100)
print(trainingdata[0].shape)
print(testdata[0].shape)

model = keras.Sequential([
    keras.layers.LSTM(64),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer=keras.optimizers.RMSprop(lr=0.05),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(trainingdata[0], trainingdata[1], epochs=100)

good = 0
bad = 0
for x in trainingdata[1]:
    if x < 1:
        good += 1
    else:
        bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))
model.save("Models/LSTM4.mdl")

loss, accu = model.evaluate(testdata[0], testdata[1])
print("Test samples accuracy:", accu)
print("Test loss accuracy:", loss)

good = 0
bad = 0
for x in testdata[1]:
   if x == 0:
      good += 1
   else:
      bad += 1
print("TEST, Good: " + str(good) + ", Bad" + str(bad))
