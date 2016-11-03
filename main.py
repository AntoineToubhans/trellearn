#!/usr/bin/env python

import sys
import src.json_importing as I
import src.json_preprocessing_naive as P
import src.data_training as T
import src.data_cross_validation as V
#import src.extract_feature as E
import src.extract_feature_multilabel as EML

if __name__ == '__main__':

    print('Hello, I am Trellearn')

    jsonFileName = sys.argv[1]

    cards = I.parseJSON(jsonFileName)

    X, Y, cv, mlb = EML.extract(cards)
    V.validateML(X, Y)

#    X, y = P.extractDataFromCards(cards)
#    V.search(X, y)

    #print(clf.predict(X[2:3]))

    exit(0)
