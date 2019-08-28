import tensorflow as tf
from tensorflow import keras
import DataProcess as dp

fro = 1
to = 20
route = "ProcessedLogs\\Splitted\\"

trainingdata = dp.loaddata_split_LSTM(route, fro, to)
print(trainingdata[0].shape)

model = keras.Sequential([
    keras.layers.Dense(65),
    keras.layers.LSTM(512),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer=keras.optimizers.RMSprop(lr=0.05),
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

model.save("Models\LSTMSplitted2.mdl")