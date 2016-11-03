import numpy as np

from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

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
        'clf': LogisticRegression(),
        'name': 'LogisticRegression',
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
    }, {
        'clf': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1),
        'name': 'Neural Network :)',
    }]

    models = [{
        'clf': OneVsRestClassifier(model["clf"]),
        'name': 'OneVsRest(%s)' % model['name'],
    } for model in simpleModels]


    for model in models:
        clf = model["clf"]
        name = model["name"]

        print(80 * '-')
        print("Validating %s" % name)
        print(80 * '-')
        print(". Params: %s" % clf.get_params())

        clf.fit(X, Y)

        scores = cross_val_score(clf, X, Y, cv=50, scoring=label_ranking_average_precision_fun)

        print(80 * '-')
        print(scores)
        print(80 * '-')
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
