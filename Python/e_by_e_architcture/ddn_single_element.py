import pandas as pd
import numpy as np
import sys
from sklearn import preprocessing
from keras.models import Model, Sequential
from keras.layers import Dense, Input, Activation
from keras.optimizers import SGD, RMSprop, Adam
from keras.regularizers import l2
import csv

timestep = 0.0333

training_set = '../data/training_set.csv'
labels = '../data/training_labels.csv'

testing_set = '../data/testing_set.csv'
test_labels = '../data/testing_labels.csv'

# LOAD data
training_df = pd.read_csv(training_set, header=0)
labels_df = pd.read_csv(labels, header=0)

training_data = training_df.loc[:,'p1x':'f4z'].values
labels_data = labels_df.loc[:,'v1x':'v4z'].values

xTrain = training_data#[0:2000000]
yTrain = labels_data#[0:2000000]

testing_df = pd.read_csv(testing_set, header=0)
tLabels_df = pd.read_csv(test_labels, header=0)

testing_data = testing_df.loc[:,'p1x':'f4z'].values
tLabels_data = tLabels_df.loc[:,'v1x':'v4z'].values

xTest = testing_data[0:1000000]
yTest = tLabels_data[0:1000000]

# standardization
scaler = preprocessing.StandardScaler().fit(xTrain)
scaler.transform(xTrain)
scaler.transform(xTest) 

num_examples = xTrain.shape[0]
num_features = xTrain.shape[1]
num_labels = yTrain.shape[1]

num_hidden_layers = 2 
layer_nodes = 200 # less than features, which is 36 for initial dataset

deep_NN = Sequential()
# input layer
deep_NN.add( Dense(layer_nodes, input_shape = (num_features,), W_regularizer=l2(0.01), init = 'glorot_uniform') )
deep_NN.add( Activation('relu') )
for i in range(num_hidden_layers):
    deep_NN.add( Dense( layer_nodes, W_regularizer=l2(0.01), init = 'glorot_uniform') )
    deep_NN.add( Activation('relu') )
# output layer
deep_NN.add( Dense(num_labels, W_regularizer=l2(0.01), init='glorot_uniform') )
deep_NN.add( Activation('linear') )

# initialize stochastic gradient descent
#sgd = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
#rms_prop = RMSprop(lr=0.0001, rho=0.9, epsilon=1e-06)
adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08) 

deep_NN.compile(loss='mse', optimizer= adam, metrics=['accuracy'])
# train
hist = deep_NN.fit(xTrain, yTrain, batch_size=20000, nb_epoch=100, validation_data=(xTest, yTest), verbose=1, shuffle=True)
y_pred = deep_NN.predict(xTrain, batch_size=20000, verbose=1)

# saving history
sys.stdout.write('history: saving to file')
with open('../training/results:(2hl,200u,200ep).csv', 'wb') as f:
    t_steps = len(hist.history['acc'])
    writer = csv.writer(f, delimiter=',' )
    writer.writerow( ('loss', 'acc', 'val_loss', 'val_acc')  )
    for i in range(t_steps):
        loss = hist.history['loss'][i]
        acc = hist.history['acc'][i]
        val_loss = hist.history['val_loss'][i]
        val_acc = hist.history['val_acc'][i]
        writer.writerow( (loss, acc, val_loss, val_acc) )    
    f.close()
sys.stdout.write('...completed\n')

#saving predictions
sys.stdout.write("predictions: saving to file: ")
indices = range( y_pred.shape[0]  )
with open('../data/testing_pred.csv', 'wb') as f:
    f.write('el,v1,v2,v3,v4,t,v1x,v1y,v1z,v2x,v2y,v2z,v3x,v3y,v3z,v4x,v4y,v4z\n')
    for i in indices:
        if i % 10000 == 0:
	    sys.stdout.write(str(i) + " - ")
	    sys.stdout.flush()
	f.write( str(int(training_df.loc[i,'el']))\
	 + "," + str(int(training_df.loc[i,'v1']))\
	 + "," + str(int(training_df.loc[i,'v2']))\
	 + "," + str(int(training_df.loc[i,'v3']))\
	 + "," + str(int(training_df.loc[i,'v4']))\
	 + "," + str(int(training_df.loc[i,'t']))\
	 + "," + str(y_pred[i][0])\
	 + "," + str(y_pred[i][1])\
	 + "," + str(y_pred[i][2])\
	 + "," + str(y_pred[i][3])\
	 + "," + str(y_pred[i][4])\
	 + "," + str(y_pred[i][5])\
	 + "," + str(y_pred[i][6])\
 	 + "," + str(y_pred[i][7])\
	 + "," + str(y_pred[i][8])\
	 + "," + str(y_pred[i][9])\
	 + "," + str(y_pred[i][10])\
	 + "," + str(y_pred[i][11]) + "\n" )
    f.close()
sys.stdout.write("...completed\n")
