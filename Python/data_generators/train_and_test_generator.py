import sys
import random
import pandas as pd

data_path = '../../data/all_v/data_set.csv'
labels_path = '../../data/all_v/labels_set.csv'

sys.stdout.write('- reading dataframes')
data_df = pd.read_csv(data_path, header=None)
labels_df = pd.read_csv(labels_path, header=None)
sys.stdout.write(' ... completed\n')

rows = data_df.shape[0]
columns = data_df.shape[1]
label_columns = labels_df.shape[1]

names = ['t']
size = (columns - 1) / 9
for i in range(1, size + 1 ):
    names.extend( ['p' + str(i) + 'x', 'p' + str(i) + 'y', 'p' + str(i) + 'z'] )
    names.extend( ['v' + str(i) + 'x', 'v' + str(i) + 'y', 'v' + str(i) + 'z'] )
    names.extend( ['f' + str(i) + 'x', 'f' + str(i) + 'y', 'f' + str(i) + 'z'] )

labels = ['t']
size = (label_columns - 1) / 3
for i in range(1, size + 1 ):
    labels.extend( ['v' + str(i) + 'x', 'v' + str(i) + 'y', 'v' + str(i) + 'z'] )

data_df.columns = names
labels_df.columns = labels

indices = range( rows )
#random.shuffle( indices )

split = 0.6
limit = int(split * rows)

header_data = data_df.columns.values
header_labels = labels_df.columns.values

# training sets
sys.stdout.write("- generating training set")
sys.stdout.flush()
training_set = data_df.iloc[ indices[0:limit] ]
training_labels = labels_df.iloc[ indices[0:limit] ]
training_set.to_csv('../../data/all_v/training_set.csv', delimiter=',', header=header_data, index=False)
training_labels.to_csv('../../data/all_v/training_labels.csv', delimiter=',', header=header_labels, index=False)
sys.stdout.write("... completed\n")

# testing sets
sys.stdout.write("- generating test set")
sys.stdout.flush()
testing_set = data_df.iloc[ indices[limit:] ]
testing_labels = labels_df.iloc[ indices[limit:] ]
testing_set.to_csv('../../data/all_v/testing_set.csv', delimiter=',', header=header_data, index=False)
testing_labels.to_csv('../../data/all_v/testing_labels.csv', delimiter=',', header=header_labels, index=False)
sys.stdout.write("... completed\n")
