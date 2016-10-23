import numpy as np

from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.multiclass import OneVsRestClassifier

from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import label_ranking_average_precision_score, make_scorer

def label_ranking_average_precision_fun(estimator, X, Y):
    return label_ranking_average_precision_score(Y, estimator.predict_proba(X))

def validateML(X, Y):
    simpleModels = [{
        'clf': MultinomialNB(),
        'name': 'Bernoulli',
    }, {
        'clf': BernoulliNB(),
        'name': 'Multinomial',
    }, {
        'clf': SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=42),
        'name': 'SGDClassifier',
    }, {
        'clf': SGDClassifier(loss='modified_huber', penalty='l2', alpha=1e-3, n_iter=5, random_state=42),
        'name': 'SGDClassifier',
    }, {
        'clf': DecisionTreeClassifier(),
        'name': 'DecisionTreeClassifier',
    }, {
        'clf': RandomForestClassifier(n_estimators=10),
        'name': 'RandomForestClassifier',
    }]

    models = [{
        'clf': OneVsRestClassifier(model["clf"]),
        'name': 'OneVsRest(%s)' % model['name'],
    } for model in simpleModels]


    for model in models:
        print(80 * '-')
        print("Validating %s" % model["name"])

        clf = model["clf"]
        clf.fit(X, Y)

        scores = cross_val_score(clf, X, Y, cv=20, scoring=label_ranking_average_precision_fun)

        print(80 * '-')
        print(scores)
        print(80 * '-')
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
