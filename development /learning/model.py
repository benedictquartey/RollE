from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D, Lambda, Conv2D

# inputshape for images
imageHeight, imageWidth, imageChannels = 66,200,3

def cnn():
    # Nvidia's convolutional neural Network architecture
    model = Sequential()
    # normalize inputs to range -1 to 1
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(imageHeight, imageWidth, imageChannels)))

    #convolutional layers for feature extraction
    model.add(Conv2D(24, (5, 5), activation="elu", strides=(2, 2)))

    model.add(Conv2D(36, (5, 5), activation="elu", strides=(2, 2)))

    model.add(Conv2D(48, (5, 5), activation="elu", strides=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation="elu"))

    model.add(Conv2D(64, (3, 3), activation="elu"))

    #dropout with probability of 0.5 to reduce overfitting
    model.add(Dropout(0.5)) 

    model.add(Flatten())

    # fully connected layers with elu activation
    model.add(Dense(100, activation='elu'))

    model.add(Dense(50, activation='elu'))

    model.add(Dense(10, activation='elu'))

    # this is the output layer
    model.add(Dense(1))

    # display model architecture 
    #model.summary()

    return model

