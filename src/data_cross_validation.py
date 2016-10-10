import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score

def validate(X, y):
    clfs = [{
        'clf': BernoulliNB(alpha=1),
        'name': 'Bernoulli',
    }, {
        'clf': MultinomialNB(alpha=1),
        'name': 'Multinomial',
    }, {
        'clf': SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42),
        'name': 'SGDClassifier',
    }]

    for o in clfs:
        scores = cross_val_score(o["clf"], X, y, cv=10)
        print("%s accuracy: %0.2f (+/- %0.2f)" % (o["name"], scores.mean(), scores.std() * 2))
