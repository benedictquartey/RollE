# for computer vision and image manipulation operations
import cv2
# for plotting visualization for model and other data statistics
import matplotlib.pyplot as plt
# import data analysis toolkit 
import pandas as pd 
#numpy for efficient matrix math
import numpy as np 
# spliting data into test and validation datasets
from sklearn.model_selection import train_test_split

import os

# inputshape for images
imageHeight, imageWidth, imageChannels = 66,200,3



def prepareData():
    # read  csv file
    data_df = pd.read_csv('data/driving_data.csv',names=['img_filename',  'steering', 'throttle', ]) 
    
    # select only camera values and corresponding steering command
    X=data_df['img_filename'].values 
    Y=data_df['steering'].values

    (X_train, X_test, Y_train, Y_test) = train_test_split(X,Y, test_size=0.2, random_state=0)

    return (X_train, X_test, Y_train, Y_test)


#confirms that all images collected in csv file actually exists in data folder
def data_check():
    if not os.path.exists("data/IMG/"):
        os.makedirs("data/IMG/")
    
    data_df = pd.read_csv('data/driving_data.csv',names=['img_filename', 'steering', 'throttle'])
        
    valid_images,invalid_images =0,0
    invalid_filenames = []

    # select only image file names
    img_filenames=data_df['img_filename'].values
    print("\n**************** Beginning Data Verification ****************")
    for filename in img_filenames:
        if isinstance(loadImage(filename), np.ndarray): #check if file loaded from filename is a numpy multidimensional array (images are represented as such)
            valid_images+=1
        else:
            invalid_images+=1
            invalid_filenames.append(filename)
    print("Valid Images: {} || Invalid Images : {}".format(valid_images,invalid_images))
    print("Invalid files are: {}\n".format(invalid_filenames))


# load images from disk given filepath
def loadImage(filename):
    return cv2.imread(filename)

# preprocessing images
def formatImage(image):
    # crop to remove upwanted parts (remove first 38 pixels from height of the image) [may want to remove this]
    img = image[38:,:,:] 
    # resize to fit input shape of model
    img = cv2.resize(img,(imageWidth, imageHeight),cv2.INTER_AREA)
    # convert to YUV colorspace
    img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) alternative colorspace might produce better results
    return img


# generate multiple training data with varied changes for better learning
def augment_data(img_filename, steering_angle, range_x=100, range_y=10):
    image = loadImage(img_filename) 

    # randomly mirroring image by flipping 
    if np.random.choice(2) == 0:
        image = cv2.flip(image, 1)
        steering_angle = np.clip(-steering_angle,-1,1)

    # # add random shadows to image
    height, width = image.shape[0], image.shape[1]
    # randomly generate size of shadow limited to width of image \
    [x1, x2] = np.random.choice(width, 2, replace=False)
    k = height / (x2 - x1)
    b = - k * x1
    # add shadow to image
    for i in range(height):
        end = int((i - b) / k)
        image[i, :end, :] = (image[i, :end, :] * .5).astype(np.int32)    

    return image, steering_angle



# only run if script if invoked directly
if __name__ == "__main__": 
    data_check()


