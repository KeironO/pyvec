import cPickle as pickle

def pickle_in(directory, file_name):
    val_data = None
    val_labels = None
    test_data = None
    test_labels = None
    train_data, train_labels, val_data, val_labels, test_data, test_labels = pickle.load(open(directory+file_name, 'rb'))
    return train_data, train_labels, val_data, val_labels, test_data, test_labels
   
  