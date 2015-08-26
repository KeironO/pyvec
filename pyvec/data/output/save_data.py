import cPickle as pickle

def pickle_data(directory, trait, train_data, train_labels, val_data=None, val_labels=None, test_data=None, test_labels=None):
    pickle.dump((train_data, train_labels, val_data, val_labels, test_data, test_labels), open(directory+"/"+trait, 'wb'))

