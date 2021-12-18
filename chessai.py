import chess
import chess.engine
from PGNToDataset import *
import tensorflow as tf
from tensorflow import keras
import numpy as np
import tensorflow.keras.layers as layers
import tensorflow.keras.optimizers as optimizers
from tensorflow.keras.optimizers import SGD

board = chess.Board()
# =============================================================================
# boardArray = []
# stockfishArray = []
# for i in range(1,3):
#     temp1, temp2 = (parsePGNToDataset("master_games" + str(i) + ".pgn"))
#     boardArray = boardArray + (temp1)
#     stockfishArray = stockfishArray + (temp2)
# 
# with open('boardArray.npy', 'wb') as f:
#     np.save(f, boardArray)
# with open('stockfishArray.npy', 'wb') as f:
#     np.save(f, stockfishArray)
# =============================================================================


with open('boardArray.npy', 'rb') as f:
    boardArray = np.load(f, allow_pickle = True)
    boardArray = np.squeeze(boardArray)
with open('stockfishArray.npy', 'rb') as f:
    stockfishArray = np.load(f, allow_pickle = True)
    stockfishArray = np.squeeze(stockfishArray)
temp = []
for i in stockfishArray:
    if(type(i) != np.int32 and type(i) != int):
        temp = temp + [0]
    else:
        temp = temp + [i]
stockfishArray = np.array(temp)
    

#train_dataset = tf.data.Dataset.from_tensor_slices((boardArray, stockfishArray))
#test_dataset = tf.data.Dataset.from_tensor_slices((boardArray, stockfishArray))

#print(test_dataset)

inputs = keras.Input(shape=(64,))

dense = layers.Dense(64, activation="relu")
x = dense(inputs)

for i in range(10):
    x = layers.Dense(64, activation="relu")(x)
outputs = layers.Dense(10)(x)

model = keras.Model(inputs=inputs, outputs=x, name="Chess_Ai")

model.summary()

opt = SGD(lr=.1)

model.compile(
    loss="mean_squared_error",
    optimizer=opt,
    metrics=["accuracy"],
)

history = model.fit(boardArray, stockfishArray, batch_size=64, epochs=15)

test_scores = model.evaluate(boardArray, stockfishArray)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

model.save("chessAi")


