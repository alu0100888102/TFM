import tensorflow as tf
from tensorflow import keras
import DataProcess as dp

fro = 1
to = 20
route = "ProcessedLogs\\Hashed\\"

trainingdata = dp.loaddata_hash(route, fro, to)
print(trainingdata)

model = keras.Sequential([
    keras.layers.Dense(6),
    keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(trainingdata[0], trainingdata[1], steps_per_epoch=91857, epochs=5)

good = 0
bad = 0
for x in trainingdata[1]:
    if x < 1:
        good += 1
    else:
        bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))

model.save("Models\DFFHashed.mdl")
