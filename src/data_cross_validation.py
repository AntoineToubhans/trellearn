import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.model_selection import cross_val_score

def validate(X, y):
    validateBernoulli(X, y)
    validateMultinomial(X, y)

def validateBernoulli(X, y):

    clf = BernoulliNB()

    scores = cross_val_score(clf, X, y, cv=10)
    print(scores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

def validateMultinomial(X, y):

    clf = MultinomialNB()

    scores = cross_val_score(clf, X, y, cv=10)
    print(scores)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
