import numpy as np
import re
from sklearn.naive_bayes import MultinomialNB

validPhoneNumber = re.compile(r"(\+33|0)[0-9]{9}$")
validMongoId = re.compile(r"(^[0-9a-f]{24}$)|(^[0-9a-f]{12})$")

def prefilterStr(str):
    str = str.lower()

    for separator in ['\t', '\n', '/', '-', ':', '...', ',', ';', '.', '(', ')', '[', ']', '\'', '_', '*', '=', '#']:
        str = str.replace(separator, ' ')

    accentPatterns = {
        'e': ['é', 'è', 'ê'],
        'a': ['à', 'â'],
    }

    for pattern in accentPatterns:
        for charToBeReplaced in accentPatterns[pattern]:
            str = str.replace(charToBeReplaced, pattern)

    return str

def mapWord(word):
    if '@' in word:
        return '_email'

    if word.startswith('http'):
        return '_url'

    if validPhoneNumber.match(word):
        return '_tel'

    if validMongoId.match(word):
        return '_mongoId'

    return word

def filterWord(word):
    if len(word) < 2:
        return False

    if word in ['du', 'de', 'du', 'elle', 'il', 'je', 'la', 'le', 'les', 'on', 'sur', 'tu']:
        return False

    return True

def extractWordsFromString(str, words):
    str = prefilterStr(str)

    for word in filter(filterWord, map(mapWord,str.split(' '))):
        if word in words:
            words[word] += 1
        else:
            words[word] = 1

def extractWordsFromCard(card, words):
    extractWordsFromString(card['name'], words)
    extractWordsFromString(card['desc'], words)

def extractWordsFromCards(cards):
    words = {}

    for card in cards:
        extractWordsFromCard(card, words)

    return words

def extractDataFromCards(cards):
    words = extractWordsFromCards(cards)

    return {
        'words': words,
        'words_count': len(words),
    }


# X = np.random.randint(5, size=(6, 100))
# y = np.array([1, 2, 3, 4, 5, 6])
# clf = MultinomialNB()
# clf.fit(X, y)
# print(clf.predict(X[2:3]))

def naiveBayesRegression(json):
    return 'ok'
