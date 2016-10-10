import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.model_selection import cross_val_score

def validate(X, y):
    clfs = [{
        'clf': BernoulliNB(alpha=0.5),
        'name': 'Bernoulli',
    }, {
        'clf': MultinomialNB(alpha=0.5),
        'name': 'Multinomial',
    }]

    for o in clfs:
        scores = cross_val_score(o["clf"], X, y, cv=20)
        print("%s accuracy: %0.2f (+/- %0.2f)" % (o["name"], scores.mean(), scores.std() * 2))
