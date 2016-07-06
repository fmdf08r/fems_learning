import csv
import sys
import pandas as pd
import random
from collections import defaultdict

filePath = "../data/obj_files/obj_info_"
ext = ".csv"

timesteps = 600
data = defaultdict(list)
labels = defaultdict(list)

sys.stdout.write("- reading the " + str(timesteps) + " files\n")
names = []
sys.stdout.write("- status: ")
for t in range(timesteps - 1):
    sys.stdout.write(str(t) + " - ")
    sys.stdout.flush()
    dataName = filePath + str(t) + ext
    labelName = filePath + str(t + 1) + ext
    with open(dataName, 'r') as r1:
        reader = csv.DictReader(r1)
        names = reader.fieldnames
        for row in reader:
            for n in names: 
                data[ n ].append( row[n] )
        r1.close()
    with open(labelName, 'r') as r2:
        reader = csv.DictReader(r2)
        names = reader.fieldnames
        for row in reader:
            for n in names:
                labels[ n ].append( row[n] )
        r2.close()
sys.stdout.write("completed\n")

sys.stdout.write("- creating dataframes")
data_df = pd.DataFrame( data )
labels_df = pd.DataFrame( labels )
sys.stdout.write("... completed\n")

rows = data_df.shape[0]
columns = data_df.shape[1]

indices = range( rows )
random.shuffle( indices )

split = 0.6
limit = int(split * rows)

# training sets
sys.stdout.write("- generating training set")
training_set = data_df.iloc[ indices[0:limit] ]
training_labels = labels_df.iloc[ indices[0:limit] ]
training_set.to_csv('../data/training_set.csv', delimiter=',', header=names, index=False)
training_labels.to_csv('../data/training_labels.csv', delimiter=',', header=names, index=False)
sys.stdout.write("... completed\n")

# testing sets
sys.stdout.write("- generating test set")
testing_set = data_df.iloc[ indices[limit:] ]
testing_labels = labels_df.iloc[ indices[limit:] ] 
testing_set.to_csv('../data/testing_set.csv', delimiter=',', header=names, index=False)
testing_labels.to_csv('../data/testing_labels.csv', delimiter=',', header=names, index=False)
sys.stdout.write("... completed\n")
