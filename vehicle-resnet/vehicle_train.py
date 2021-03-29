#importing the libraries 
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Activation
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam, RMSprop, Adagrad, Adamax, SGD
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import get_file
from os.path import join, dirname, basename
from sklearn.model_selection import train_test_split
import pandas as pd
import glob

import random

url = 'https://storage.googleapis.com/vehicle-dataset/vehicles_full.zip'
path_to_zip =get_file('vehicles_full.zip', origin=url, extract=True)
path = join(dirname(path_to_zip), 'vehicles_full')

files = glob.glob(path + '/*/*', recursive=True)
  
X = files
y = [basename(dirname(f)) for f in files]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_df = pd.DataFrame({"filename": X_train, "class": y_train}) 
test_df = pd.DataFrame({"filename": X_test, "class": y_test})

IMG_HEIGHT = 32 
IMG_WIDTH = 64
batch_size = 64
class_names = ['Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6']
image_generator = ImageDataGenerator(rescale=1./255,
                                     width_shift_range=.15,
                                     height_shift_range=.15,
                                     brightness_range=(0.1,0.9),
                                     zoom_range=0.3,
                                     channel_shift_range=150,
                                     horizontal_flip=True,
                                     validation_split=0.2) 

train_data_gen = image_generator.flow_from_dataframe(dataframe=train_df,
                                                     x_col="filename",
                                                     y_col="class",
                                                     subset="training",
                                                     shuffle=True,
                                                     seed=42,
                                                     batch_size=batch_size,
                                                     classes=class_names,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode="categorical")
valid_data_gen = image_generator.flow_from_dataframe(dataframe=train_df,
                                                     x_col="filename",
                                                     y_col="class",
                                                     subset="validation",
                                                     shuffle=True,
                                                     seed=42,
                                                     batch_size=batch_size,
                                                     classes=class_names,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode="categorical")

test_image_generator = ImageDataGenerator(rescale=1./255) 
test_data_gen = test_image_generator.flow_from_dataframe(dataframe=test_df,
                                                         x_col="filename",
                                                         y_col="class",
                                                         shuffle=False,
                                                         classes=class_names,
                                                         target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                         class_mode="categorical")


model_top = ResNet50(
    include_top=False,
    weights=None,
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))
x = GlobalAveragePooling2D()(model_top.output)  
x = Dropout(0.2)(x)
x = Dense(128)(x)
x = Dense(6)(x)
x = Activation('softmax')(x)
model = Model(model_top.input, x, name='resnet50')

early_stop = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, verbose=1)

model.compile(optimizer=RMSprop(lr=0.001),
              loss=CategoricalCrossentropy(),
              metrics=['accuracy'])



model.summary()
model.save("./models/resnet.v1.h5")

model = model.fit(train_data_gen,validation_data=valid_data_gen,epochs=5,callbacks=[early_stop, reduce_lr])



