#!/usr/bin/env python

import sys
import src.json_importing as I
import src.json_preprocessing_naive as P
import src.data_training as T
import src.data_cross_validation as V
import src.extract_feature as E

if __name__ == '__main__':

    print('Hello, I am Trellearn')

    jsonFileName = sys.argv[1]

    cards = I.parseJSON(jsonFileName)

    X, y = E.extract(cards)

#    X, y = P.extractDataFromCards(cards)
    V.search(X, y)

    #print(clf.predict(X[2:3]))

    exit(0)
