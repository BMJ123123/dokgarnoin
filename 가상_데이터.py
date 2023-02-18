# %%
from modules.orm import SensorData
s0 = SensorData.get_by_type(0)
s1 = SensorData.get_by_type(1)
s2 = SensorData.get_by_type(2)
s3 = SensorData.get_by_type(3)
print(len(s0), len(s1), len(s2), len(s3), sep="\n\n")
# %%
import numpy as np
from random import shuffle
from tensorflow.keras.utils import to_categorical
def data_to_numpy(s):
    return np.array([[v.min, v.max, v.avg] for v in s]), np.array([[v.type] for v in s])
value_x = np.empty((0, 3))
value_y = np.empty((0, 4))
s = s0 + s1 + s2 + s3
shuffle(s)
x, y = data_to_numpy(s)
value_x = np.append(value_x, x, axis=0)
value_y = np.append(value_y, to_categorical(y, num_classes=4), axis=0)
# %%
split_rate = len(value_x)*3//4
value_x_train, value_x_test = value_x[:split_rate], value_x[split_rate:]
value_y_train, value_y_test = value_y[:split_rate], value_y[split_rate:]

# %%
from tensorflow.keras import layers, Sequential
model = Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(3, )))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))
model.compile(metrics=['accuracy'], loss='categorical_crossentropy')
model.summary()
# %%
histroy = model.fit(value_x_train, value_y_train, batch_size=512, epochs=100, validation_data=(value_x_test, value_y_test))
# %%
model.predict(np.array([value_x_train[0]]))
# %%
from matplotlib import pyplot as plt
plt.scatter([s.max/4096 for s in (s0+s1+s2+s3)], [s.type for s in (s0+s1+s2+s3)])
# plt.xscale('log')
plt.show()
# %%
