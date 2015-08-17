import cPickle as pickle

def pickle_data(directory, train_data, train_labels, val_data, val_labels, test_data=None, test_labels=None):
    print directory
    out = file(directory+"/pdata.p", 'wb')
    pickle.dump((train_data, train_labels, val_data, val_labels, test_data, test_labels), out, protocol=pickle.HIGHEST_PROTOCOL)
    out.close()
