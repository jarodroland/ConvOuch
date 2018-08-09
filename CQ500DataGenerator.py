import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, ID_list, batch_size=14, dim=(224, 224), n_channels=3, shuffle=True): #n_classes=1, 
        'Initialization'
        self.data_dir = '/Users/zhengma/Documents/ConvOuch/Data/'
        self.dim = dim
        self.batch_size = batch_size
        self.ID_list = ID_list
        self.n_channels = n_channels
        # self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()


    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.ID_list) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        batch_list_IDs = [self.ID_list[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(batch_list_IDs)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.ID_list))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, batch_list_IDs):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        batch_samples = np.empty((self.batch_size, *self.dim, self.n_channels))
        batch_labels = np.empty((self.batch_size), dtype=int)

        # load the data
        for i, ID in enumerate(batch_list_IDs):
            # load sample
            batch_samples[i,] = np.load(self.data_dir + 'Slices/' + ID + '.npy')

            # load label
            data_obj = np.load(self.data_dir + 'Labels/' + ID + '.npy')
            data_dict = data_obj.item()
            batch_labels[i] = int(data_dict['label'])


        # return batch_samples, keras.utils.to_categorical(batch_labels, num_classes=self.n_classes)
        return batch_samples, batch_labels



