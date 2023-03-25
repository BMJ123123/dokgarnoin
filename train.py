# %%
from modules.db import DBHandler
from modules.orm import *
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
env.MAIN_DB_NAME = "koin.db"
# vals = [sorted(s.decode_audio()) for s in SensorData.get(201239)]

# for val in vals[-10:]:
#     plt.plot(val)
#     plt.show()
    
# %%
vals = SensorData.get(201239)
print(len(vals))
vals = [val for val in vals if val.sound_type is not None]
print(len(vals))
# %%
print(vals[0])

from random import shuffle
shuffle(vals)
# %%
train_x = np.array([sorted(val.decode_audio()) for val in vals]) / 4096
train_y = [val.sound_type for val in vals]
train_y = tf.keras.utils.to_categorical(train_y)


print(train_x[0], train_y[0])

# %%
split_rate = len(train_x)*3//4
train_x_train, train_x_test = train_x[:split_rate], train_x[split_rate:]
train_y_train, train_y_test = train_y[:split_rate], train_y[split_rate:]
# %%
from tensorflow.keras import layers, Sequential
model = Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(len(train_x[0]), )))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))
model.compile(metrics=['accuracy'], loss='categorical_crossentropy')
model.summary()

# %%
history = model.fit(train_x_train, train_y_train, batch_size=256, epochs=50, validation_data=(train_x_test, train_y_test))

# %%
import matplotlib.pyplot as plt
fig, loss_ax = plt.subplots(figsize=(16, 9))

acc_ax = loss_ax.twinx()

loss_ax.plot(history.history['loss'],'b',label='train loss')
loss_ax.plot(history.history['val_loss'],'b--',label='val loss')
acc_ax.plot(history.history['accuracy'],'r',label='train acc')
acc_ax.plot(history.history['val_accuracy'],'r--',label='val acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuracy')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')
plt.show()
# %%
non_vals = SensorData.get(201239)
non_vals = [sorted(val.decode_audio()) for val in non_vals if val.sound_type is None]
non_vals

# vals = [sorted(s.decode_audio()) for s in SensorData.get(201239)]
data_class = ['silence', 'neutral', 'noisy']
for val in non_vals[-100:]:
    x = np.array(val)
    x = np.expand_dims(x, axis=0)
    s = model.predict([val], verbose=0)
    result = data_class[s.argmax()]
    print(result)
    plt.plot(val)
    plt.show()

# %%
from random import shuffle
vals = SensorData.get(201239)
vals = [val for val in vals if val.sound_type is not None]
shuffle(vals)
cnt = 0
for val in vals:
    x = sorted(val.decode_audio())
    x = np.array(x) / 4096
    x = np.expand_dims(x, axis=0)
    s = model.predict([x], verbose=0)
    result = data_class[s.argmax()]
    if (result != data_class[val.sound_type]):
        cnt += 1
print(f"{cnt/len(vals)*100:.1f}")
# %%
model.save('model.h5')
# %%
