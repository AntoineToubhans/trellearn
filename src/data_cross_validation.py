import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

def validate(X, y):

    test_size = 0.4

    for i in range(0, 10):

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.1,
            random_state=i
        )

        clf = MultinomialNB()
        clf.fit(X_train, y_train)

        score = clf.score(X_test, y_test)

        print("[#%d] Score for cross-validating among %.2f of the data: %.3f" % (i, 100 * test_size, score))
