from sklearn                         import preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import re

validPhoneNumber = re.compile(r"(\+33|0)[0-9]{9}$")
validMongoId = re.compile(r"(^[0-9a-f]{24}$)|(^[0-9a-f]{12})$")

def flattenCards(cards):
    result = []

    for card in cards:
        datum = card["name"] + ' ' + card["desc"]
        for label in card.get("idLabels", []):
            result.append({
                'datum': datum,
                'label': label
            })

    return result

def removeThreshold(threshold, cards):
    labelDic = {}
    for card in cards:
        labelDic[card["label"]] = labelDic.get(card["label"], 0) + 1

    return filter(lambda x: labelDic[x["label"]] > threshold, cards)

def prepareCards(cards):
    cards = flattenCards(cards)
    cards = removeThreshold(10, cards)

    data, labels = [], []
    for card in cards:
        data.append(card["datum"])
        labels.append(card["label"])

    return data, labels

def tokenize_word(word):
    if '@' in word:
        return '_email'

    if word.startswith('http'):
        return '_url'

    if validPhoneNumber.match(word):
        return '_tel'

    if validMongoId.match(word):
        return '_mongoId'

    return word


def custom_tokenizer(s):
    tokens = s.split()

    return map(tokenize_word, tokens)

def extractData(data):
    count_vectorizer = CountVectorizer(tokenizer=custom_tokenizer)

    X_raw = count_vectorizer.fit_transform(data)

    X_tf = TfidfTransformer(use_idf=False).fit_transform(X_raw)

    return X_tf

def extractLabels(labels):
    label_encoder = preprocessing.LabelEncoder()

    return label_encoder.fit_transform(labels)

def extract(cards):
    print("Preparing %d cards" % len(cards))
    data, labels = prepareCards(cards)
    print("Extracting features from %d cards" % len(data))

    X = extractData(data)
    y = extractLabels(labels)

    print("Extraction ok: X %s, y %s" % (X.toarray().shape, y.shape))

    return X, y
