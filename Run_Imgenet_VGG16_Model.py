import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.layers import Conv2D

from keras.layers import MaxPool2D
from keras.layers import Flatten

from keras.optimizers import Adam

from keras.layers import Dropout

from keras.applications.vgg16 import VGG16
from keras.utils.vis_utils import plot_model

from keras.applications.vgg16 import decode_predictions


num_train_set = 40


#add our own fully connected layers for the final classification

# create the base pre-trained model
base_model = VGG16(include_top=False, weights='imagenet', 
                    input_tensor=None, input_shape=(224, 224, 3), pooling=None)

x = base_model.output
#flattentit
x = Flatten()(x)
# let's add a fully-connected layer
x = Dense(4096, activation='relu')(x)
#another fully-connected layer
x = Dense(4096, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(1, kernel_initializer='normal', activation='sigmoid')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

#now we can start to fine-tune the model
# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False
    
# compile the model (should be done *after* setting layers to non-trainable)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


for i in range(0, num_train_set):
    train_img_file = 'Train/train' + str(i+1) + '_img.npy'
    train_label_file = 'Train/train' + str(i+1) + '_label.npy'
    
    train_img = np.load(train_img_file)
    train_label = np.load(train_label_file)


    model.fit(train_img, train_label, validation_split=0.1, epochs=1, batch_size=5)
    
model.save('FirstModel.h5')
