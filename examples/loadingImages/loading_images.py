import imp, os.path as path


image_preprocesser = imp.load_source('preprocess', '../../pyvec/images/image_preprocessor.py')
dataset = imp.load_source('dataset', '../../pyvec/images/dataset.py')

directory = "./dataset/originalData/"
custom_dir = "preProcessed/"
custom_height = 64
custom_width = 64
save_path = path.abspath(path.join(directory, "../", custom_dir))
num_classes = 2
num_training_data = 10
num_validation_data = 2

split = 0.9


image_preprocesser.preprocess(directory, custom_dir, custom_height, custom_width)

train_data, train_label, val_data, val_label= dataset.vectorise(save_path,num_classes,custom_height,
                                                                custom_width, split)
nb_train = len(train_label)
nb_validation = len(val_label)
print( 'train samples:',nb_train, 'validation samples:',nb_validation)

print('Train data shape:', train_data.shape)
print('Validation data shape:', val_data.shape)