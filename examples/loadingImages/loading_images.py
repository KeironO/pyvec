import imp, os.path as path

def split_train_and_validation(save_path, custom_height, custom_width, split, test):
    train_data, train_label, val_data, val_label = pyvec_api.load_images(save_path, custom_height,
                                                                    custom_width, split, test)

    print "Train data shape:", train_data.shape
    print "Validation data shape:", val_data.shape


def split_train_validation_and_test(save_path, custom_height, custom_width, split, test):
    train_data, train_label, val_data, val_label, test_data, test_label = pyvec_api.load_images(save_path,
                                                    custom_height, custom_width, split, test)
    print "Train data shape:", train_data.shape
    print "Validation data shape:", val_data.shape
    print "Test data shape:", test_data.shape


if __name__== "__main__":

    pyvec_api = imp.load_source('api', '../../pyvec/core/api.py')

    directory = "./dataset/originalData/"
    custom_dir = "preProcessed/"
    save_path = path.abspath(path.join(directory, "../", custom_dir))

    custom_height = 64
    custom_width = 64
    split = 0.7

    print "Providing you with training and validation data! \n"
    split_train_and_validation(save_path, custom_height, custom_width, split, test=False)
    print "\nProviding you with testing too! \n"
    split_train_validation_and_test(save_path, custom_height, custom_width, split, test=True)
