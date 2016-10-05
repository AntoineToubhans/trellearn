import numpy as np
import re

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

def extractWordsFromString(str):
    str = prefilterStr(str)

    return list(filter(filterWord, map(mapWord,str.split(' '))))


def extractWordsFromCard(card):
    return {
        "id": card["id"],
        "name": extractWordsFromString(card.get("name", '')),
        "desc": extractWordsFromString(card.get("desc", '')),
        "labels": card.get("idLabels", []),
    }

def extractWordsFromCards(cards):
    return map(extractWordsFromCard, cards)

def dicEmpty():
    return {
        'next': 1,
        'entries': {}
    }

def dicGet(dic, word):
    if not word in dic["entries"]:
        dic["entries"][word] = dic["next"]
        dic["next"] += 1

    return dic["entries"][word]

def extractDataFromCardWords(maxName, maxDesc, wordDic, labelDic, X, y, cardWords):
    vectorX = np.array([0 for i in range(0, maxName + maxDesc)])

    nameWords = cardWords["name"]
    for i in range(0, len(nameWords)):
        vectorX[i] = dicGet(wordDic, nameWords[i])

    descWords = cardWords["desc"]
    for i in range(0, len(descWords)):
        vectorX[maxName + i] = dicGet(wordDic, descWords[i])

    for label in cardWords["labels"]:
        X.append(vectorX)
        y.append(dicGet(labelDic, label))

def extractMaxLengthsFromWords(words):
    maxName = 0
    maxDesc = 0
    for cardWords in words:
        maxName = max(maxName, len(cardWords["name"]))
        maxDesc = max(maxDesc, len(cardWords["desc"]))

    print("Max lenghts for 'name' is %d" % maxName)
    print("Max lenghts for 'desc' is %d" % maxDesc)

    return maxName, maxDesc

def extractDataFromWords(words):
    maxName, maxDesc = extractMaxLengthsFromWords(words)

    wordDic = dicEmpty()
    labelDic = dicEmpty()

    X = []
    y = []

    for cardWords in words:
        extractDataFromCardWords(maxName, maxDesc, wordDic, labelDic, X, y, cardWords)

    return X, y

def extractDataFromCards(cards):
    # filter card that have at least one label and extract words
    words = list(extractWordsFromCards(filter(lambda card: card["idLabels"], cards)))

    X, y = extractDataFromWords(words)

    return np.array(X), np.array(y)
