import cPickle as pickle

def pickle_data(directory, train_data, train_labels, val_data, val_labels, test_data=None, test_labels=None):
    pickle.dump((train_data, train_labels, val_data, val_labels, test_data, test_labels), open(directory+"/pdata.p", 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

