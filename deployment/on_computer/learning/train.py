
# @Author Benedict Quartey

# Import dependencies

# for plotting visualization for model and other data statistics
import matplotlib.pyplot as plt
import numpy as np 
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam

import model as NNmodel
import plots as plot
import data_processing


# hyperparameter definitions
batch_size = 100
samplesPerEpoch = 200000

epoch_steps=samplesPerEpoch // batch_size #`steps_per_epoch` is the number of batches to draw from the generator at each epoch. so if we want to train on 2000 samples each epoch and our batch size is 100, steps per epoch would be 20. So having a steps_per_epoch of 2000 means we want to trains on (2000*100) images an epoch

epochNum = 10
learningRate = 1.0e-4

# inputshape for images
imageHeight, imageWidth, imageChannels = 66,200,3

# seeding to enable exact reproduction of learning results
np.random.seed(0)



def batch_generator( imgfilepath, steering_angles, batch_size, mode):
# python generator to generate validation and training image and steering angle sets in runtime without storing
 # in memory
    images = np.empty([batch_size, imageHeight, imageWidth, imageChannels])
    steers = np.empty(batch_size)
    while True:
        i = 0
        for index in np.random.permutation(imgfilepath.shape[0]):
            center = imgfilepath[index]
            steering_angle = np.clip(steering_angles[index],-1,1)
            # only augment data when training and  augment only roughly half of the timee
            if (mode =="train" and np.random.rand() < 0.6):
                image, steering_angle = data_processing.augment_data(center, steering_angle)
            else:
                # when not training (ie when validating) only load original camera images
                image = data_processing.loadImage(center) 
            images[i] = data_processing.formatImage(image)
            steers[i] = steering_angle
            i += 1
            if i == batch_size:
                break
        yield images,steers



def data_distribution_check(samplesize,mode):
    # draw a chart showing distribution of each subsample of data generated by the batch_generator
    x_train, x_test, y_train, y_test=data_processing.prepareData()
    data_generator = batch_generator(x_train, y_train,samplesize,mode)
    y_train = next(data_generator)[1]
    plt.figure(figsize=(16,8))
    num_bins = samplesize
    # the histogram of the data
    n, bins, patches = plt.hist(y_train, num_bins)
    plt.title('Steering Angle Frequency')
    plt.xlabel('Steering Angle')
    plt.ylabel('Number of Images')
    plt.show()



def train_model():
    x_train, x_test, y_train, y_test=data_processing.prepareData()

    # import neural network model architecture 
    model = NNmodel.cnn()
    # display model architecture 
    model.summary()

# code to train model on data

 # callback function to be executed after every training epoch, only saves the trsined model
 # if its validation mean_squared_error is less than the model from the previoud epoch
    interimModelPoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                    monitor='val_loss',
                                    verbose=0,
                                    save_best_only = 'true',
                                    mode = 'auto')

    # define cost function type to be mean_squared_error
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=learningRate),metrics=['accuracy'])

    # train model
    model_history=model.fit_generator(
                        generator = batch_generator(x_train, y_train,batch_size,"train"),
                        steps_per_epoch = epoch_steps,
                        epochs=epochNum,
                        max_queue_size=1,
                        validation_data=batch_generator(x_test, y_test,batch_size,"validate"),
                        validation_steps = len(x_test),
                        callbacks = [interimModelPoint],
                        verbose = 1)


    plot.mean_square_error(model_history)
    plot.model_accuracy(model)


    # print history with all loss and accuracy values
    print(model_history.history)


        

# only run if script if invoked directly
if __name__ == "__main__":
    #uncomment the code below to view graphs of the distribution of training data
    #data_distribution_check(batch_size,"train")

    #uncomment the code below to train neural network
    train_model()



