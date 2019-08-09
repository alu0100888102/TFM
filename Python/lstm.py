import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.contrib import layers

print("Hello world")
n_clases = 1
n_values = 9


def lstmBuilder(n_neurons):

    layer = layers.fully_connected()
    lstm = rnn.BasicLSTMCell(n_neurons)

