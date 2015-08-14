import imp

image_preprocesser = imp.load_source('preprocess', '../../pyvec/images/image_preprocessor.py')
dataset = imp.load_source('dataset', '../../pyvec/images/dataset.py')

directory = "./dataset"
custom_dir = directory + "/preProcessed"
custom_height = 64
custom_width = 64

num_classes = 2
num_training_data = 10
num_validation_data = 2

image_preprocesser.preprocess(directory, custom_height, custom_width)

train_data, train_label, val_data, val_label= dataset.vectorise(custom_dir,num_classes,custom_height,
                                                                custom_width,num_training_data,num_validation_data)

print('Train data shape:', train_data.shape)
print('Validation data shape:', val_data.shape)