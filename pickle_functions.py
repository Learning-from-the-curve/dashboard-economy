import pickle
from pathlib import Path
import os

#The pickle functions are used by other scripts to store and load data in/from the pickles_jar.

def picklify(data, name):
    '''
    writes a pickle file in the pickles_jar folder with name = 'name' and content = dataframe
    input:
    generic data type containing information
    string containing the name of the file
    '''
    file_write = open(f"./pickles_jar/{name}.pkl", 'wb')
    pickle.dump(data, file_write)
    file_write.close()

def unpicklify(name):
    '''
    loads a pickle file from the pickles_jar folder with name = 'name'
    input:
    string containing the name of the file
    '''

    pickle_path = Path.cwd() / 'pickles_jar'
    file_read = open(str(pickle_path) + os.sep + name + '.pkl', 'rb')
    dataframe = pickle.load(file_read)
    file_read.close()
    return dataframe