import numpy as np
from sklearn.naive_bayes import MultinomialNB

def train(X, y):
    clf = MultinomialNB()
    clf.fit(X, y)

    return clf
