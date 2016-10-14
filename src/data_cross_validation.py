import pprint
import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV

pp = pprint.PrettyPrinter(width=80)

def validate(X, y):
    clfs = [{
        'clf': BernoulliNB(alpha=1e-3),
        'name': 'Bernoulli',
    }, {
        'clf': MultinomialNB(alpha=1e-3),
        'name': 'Multinomial',
    }, {
        'clf': SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42),
        'name': 'SGDClassifier',
    }]

    for o in clfs:
        scores = cross_val_score(o["clf"], X, y, cv=10)
        print("%s accuracy: %0.2f (+/- %0.2f)" % (o["name"], scores.mean(), scores.std() * 2))

def search(X, y):
    models = [{
        'clf': BernoulliNB(),
        'name': 'Bernoulli',
        'grid': {
            'alpha': [1e-3, 1e-2, 1e-1, 1, 1e+1, 1e+2, 1e+3],
        }
    }, {
        'clf': MultinomialNB(alpha=1e-3),
        'name': 'Multinomial',
        'grid': {
            'alpha': [1e-3, 1e-2, 1e-1, 1, 1e+1, 1e+2, 1e+3],
        }
    }, {
        'clf': SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42),
        'name': 'SGDClassifier',
        'grid': {
            'alpha': [1e-3, 1e-2, 1e-1, 1, 1e+1, 1e+2, 1e+3],
        }
    }]

    for model in models:
        clf = GridSearchCV(model["clf"], model["grid"])
        clf.fit(X, y)
        print(model["name"])
        pp.pprint(clf.cv_results_)
        print(80 * '-')
