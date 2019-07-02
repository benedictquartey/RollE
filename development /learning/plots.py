# for plotting visualization for model and other data statistics
import matplotlib.pyplot as plt


def mean_square_error(model_history):
#plot to visualize performance (training & validation loss) of all models trained at each epoch, helps identify overfitting
    plt.plot(model_history.history['loss'])
    plt.plot(model_history.history['val_loss'])
    plt.title('CNN Model MSE loss Chart')
    plt.ylabel('Mean squared error')
    plt.xlabel('Epoch no.')
    plt.legend(['Training set', 'Validation set'], loc='upper right')
    plt.show()  


def model_accuracy(model_history):
 #plot to visualize performance (training & validation accuracy) of all models trained at each epoch, helps identify overfitting
    plt.plot(model_history.history['acc'])
    plt.plot(model_history.history['val_acc'])
    plt.title('CNN Model Accuracy Chart')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch no.')
    plt.legend(['Training set', 'Validation set'], loc='upper right')
    plt.show()
