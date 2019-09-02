import tensorflow as tf
from tensorflow import keras
import DataProcess as dp

fro = 1
to = 20
route = "ProcessedLogs/Splitted/"

trainingdata = dp.loaddata_split_LSTM_moving(route, fro, to, 100)
print(trainingdata[0].shape)
print(trainingdata[1].shape)

model = keras.Sequential([
    keras.layers.Dense(61),
    keras.layers.LSTM(512),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer=keras.optimizers.Adagrad(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(trainingdata[0], trainingdata[1], epochs=200)

good = 0
bad = 0
for x in trainingdata[1]:
    if x < 1:
        good += 1
    else:
        bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))

model.save("Models/LSTMSplittedTemporal_50.mdl")
