import imp, os.path as path

def split_train_and_validation(save_path, custom_height, custom_width, split, test):
    train_data, train_label, val_data, val_label, nb_classes, image_labels = pyvec_api.load_images_and_split(save_path, custom_height,
                                                                                                             custom_width, split, test)

    print "Train data shape:", train_data.shape
    print "Validation data shape:", val_data.shape


def split_train_validation_and_test(save_path, custom_height, custom_width, split, test):
    train_data, train_label, val_data, val_label, test_data, test_label, nb_classes, image_labels = pyvec_api.load_images_and_split(save_path,
                                                                                                                                    custom_height, custom_width, split, test)
    print "Train data shape:", train_data.shape
    print "Validation data shape:", val_data.shape
    print "Test data shape:", test_data.shape

def load_image_data(save_path, custom_height, custom_width):
    data, label, image_labels = pyvec_api.load_images(save_path, custom_height, custom_width)

    print "Data shape:", data.shape

if __name__== "__main__":

    pyvec_api = imp.load_source('api', '../../pyvec/core/api.py')

    save_path = "./dataset/originalData/"

    custom_height = 8
    custom_width = 8
    split = 0.7

    print "Providing you with just the data! \n"
    load_image_data(save_path, custom_height, custom_width)

    print "\nProviding you with training and validation data! \n"
    with_test = False
    split_train_and_validation(save_path, custom_height, custom_width, split, with_test)
    print "\nProviding you with testing too! \n"
    with_test = True
    split_train_validation_and_test(save_path, custom_height, custom_width, split, with_test)
