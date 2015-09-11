import imp, os



relative_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pyvec/data/images/loader.py'))

images = imp.load_source('loader', relative_dir)

def load_images(directory,height, width):
    data, labels, names = images.load_images(directory, height, width)
    return data, labels, names

def load_images_and_split(directory, height, width, split, with_test):
    nb_classes = len([classes for classes in os.listdir(directory) if os.path.isdir(directory)])
    if with_test == False:
        train_data, train_label, val_data, val_label, images_names = images.vectorise(directory, nb_classes, height, width, split, with_test=False)
        return train_data, train_label, val_data, val_label, images_names, nb_classes
    elif with_test == True:
        train_data, train_label, val_data, val_label, test_data, test_label, images_names = images.vectorise(directory, nb_classes, height, width, split, with_test=True)
        return train_data, train_label, val_data, val_label, test_data, test_label, images_names, nb_classes
