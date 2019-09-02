import tensorflow as tf
from tensorflow import keras
import DataProcess as dp

fro = 1
to = 20
route = "ProcessedLogs\\Splitted\\"

testdata = dp.loaddata_split_LSTM(route, 21, 25, 100)

print(testdata[0].shape)
print(testdata[1].shape)


model = keras.models.load_model("Models\\LSTMSplitted2.mdl")

loss, accu = model.evaluate(testdata[0], testdata[1])
print("Test samples accuracy:", accu)
print("Test loss accuracy:", loss)

good = 0
bad = 0
for x in testdata[1]:
    if x < 1:
        good += 1
    else:
        bad += 1

print("Good: " + str(good) + ", Bad: " + str(bad))