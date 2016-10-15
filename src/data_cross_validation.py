import pprint
import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV

pp = pprint.PrettyPrinter(width=80)

def custom_score(estimator, X, Y):
    print(80 * '=')
    print(X)
    print(80 * '=')
    print(Y)
    print(80 * '=')
    print(estimator.predict_proba(X))
    print(80 * '=')
    return 1

def validateML(X, Y):
    models = [{
        'clf': MultinomialNB(),
        'name': 'Bernoulli',
    }, {
        'clf': BernoulliNB(),
        'name': 'Multinomial',
    }]

    multilabel_classifiers = [{
        'class': OneVsRestClassifier,
        'name': 'OneVsRest'
    }]

    for model in models:
        for multilabel_classifier in multilabel_classifiers:
            print(80 * '-')
            print("Validating %s %s" % (multilabel_classifier["name"], model["name"]))

            clf = multilabel_classifier["class"](model["clf"])
            clf.fit(X, Y)

            scores = cross_val_score(clf, X, Y, cv=10, scoring=custom_score)
            print(80 * '-')
            print(scores)
            print(80 * '-')
            print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

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
