import imp, os

images = imp.load_source('loader', '../../pyvec/data/images/loader.py')

def load_images(directory, height, width, split, with_test):
    nb_classes = len([classes for classes in os.listdir(directory) if os.path.isdir(directory)])
    if with_test == False:
        train_data, train_label, val_data, val_label = images.vectorise(directory, nb_classes, height, width, split, with_test=False)
        return train_data, train_label, val_data, val_label
    elif with_test == True:
        train_data, train_label, val_data, val_label, test_data, test_label = images.vectorise(directory, nb_classes, height, width, split, with_test=True)
        return train_data, train_label, val_data, val_label, test_data, test_label