import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

def train(X, Y):
    print('Training !')
    clf = OneVsRestClassifier(LogisticRegression())
    clf.fit(X, Y)

    return clf
