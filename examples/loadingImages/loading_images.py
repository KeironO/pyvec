import imp, os.path as path

def load_from_pickle(save_path):
    serialised_dir = path.abspath(path.join(save_path, "../"))
    train_data, train_labels, val_data, val_labels, test_data, test_labels = input.pickle_in(serialised_dir);
    return train_data, train_labels, val_data, val_labels, test_data, test_labels

def preprocess_images(directory, custom_dir, custom_height, custom_width):
    image_preprocesser.preprocess(directory, custom_dir, custom_height, custom_width)

def serialise_to_pickle(save_path, train_data, train_label, val_data, val_label, test_data, test_label):
    serialised_dir = path.abspath(path.join(save_path, "../"))
    output.pickle_data(serialised_dir, train_data, train_label, val_data, val_label, test_data, test_label)

def split_train_and_validation(directory, num_classes, custom_height, custom_width, split):
    train_data, train_label, val_data, val_label = dataset.vectorise(save_path,num_classes,custom_height,
                                                                    custom_width, split)
    nb_train = len(train_label)
    nb_validation = len(val_label)

    print( 'train samples:',nb_train, 'validation samples:',nb_validation)

    print('Train data shape:', train_data.shape)
    print('Validation data shape:', val_data.shape)


def split_train_validation_and_test(save_path, num_classes, custom_height, custom_width, split):
    train_data, train_label, val_data, val_label, test_data, test_label = dataset.vectorise(save_path,
                                                    num_classes,custom_height, custom_width, split, True)
    nb_train = len(train_label)
    nb_validation = len(val_label)
    nb_test = len(test_label)

    print('train samples:',nb_train, 'validation samples:',nb_validation, 'test samples', nb_test)

    print('Train data shape:', train_data.shape)
    print('Validation data shape:', val_data.shape)
    print('Test data shape:', test_data.shape)

    print "\nSaving it to file! \n"
    serialise_to_pickle(save_path, train_data, train_label, val_data, val_label, test_data, test_label)

def load_example(save_path):
    train_data, train_labels, val_data, val_labels, test_data, test_labels = load_from_pickle(save_path)
    print('Train data shape:', train_data.shape)
    print('Validation data shape:', val_data.shape)
    print('Test data shape:', test_data.shape)


if __name__== "__main__":

    image_preprocesser = imp.load_source('preprocess', '../../pyvec/images/preprocessor.py')
    dataset = imp.load_source('dataset', '../../pyvec/images/loader.py')
    output = imp.load_source('output', '../../pyvec/output/save_data.py')
    input = imp.load_source('input', '../../pyvec/input/load_data.py')

    directory = "./dataset/originalData/"
    custom_dir = "preProcessed/"
    save_path = path.abspath(path.join(directory, "../", custom_dir))

    custom_height = 64
    custom_width = 64
    split = 0.9
    num_classes = 2

    print "Providing you with training and validation data! \n"
    split_train_and_validation(save_path, num_classes, custom_height, custom_width, split)
    print "\nProviding you with testing too! \n"
    split_train_validation_and_test(save_path, num_classes, custom_height, custom_width, split)
    print "Loading in data from a serialised pickle file. \n"
    load_example(save_path)
