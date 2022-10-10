import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

data_dir = "/home/richard/School/research/nnf2sdd2/testing/0-1digits/train-0-1.txt"
dataset=pd.read_csv(data_dir)
train_features = dataset
train_labels = train_features.pop("1.48")


model = LogisticRegression()
classifier = model.fit(train_features,train_labels)
train_accuracy = 100*classifier.score(train_features,train_labels)
print("LogisticRegression: %.8f%% (training accuracy)" % (train_accuracy,))


A = np.array(train_features)
y = np.array(train_labels)
w = np.array(model.coef_).T 
b = np.array(model.intercept_) 
sum((A@w >= -b).flatten() == y)/len(y) #check for training accuracy


#creating file
arr = model.coef_[0]
file1 = open("/home/richard/School/research/nnf2sdd2/examples/0-1digits.neuron","w")
file1.write("name: example")
file1.write("\nsize: ")
file1.write((str)(len(model.coef_[0])))
file1.write("\nweights: ")
for x in range(len(arr)):
    file1.write(" ")
    file1.write(str(model.coef_[0][x]))
                    
file1.write("\nthreshold: ")
file1.write(str(model.intercept_[0]))