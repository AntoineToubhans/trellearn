from sklearn                         import preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import re

re_phone_number = re.compile(r"(\+33|0)[0-9]{9}$")
re_mongo_id = re.compile(r"(^[0-9a-f]{24}$)|(^[0-9a-f]{12})$")

def flattenCards(cards):
    result = []

    for card in cards:
        for label in card.pop("idLabels", []):
            cardForLabel = card.copy()
            cardForLabel["label"] = label
            result.append(cardForLabel)

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
        labels.append(card.pop("label"))
        data.append(card)

    return data, labels

def token_map(token):
    if '@' in token:
        return '_email'

    if token.startswith('http'):
        return '_url'

    if re_phone_number.match(token):
        return '_tel'

    if re_mongo_id.match(token):
        return '_mongoId'

    if token.startswith('└'):
        return '_hierarchy'

    return token

def token_filter(token):
    if len(token) < 2:
        return False

    if token in ['du', 'de', 'du', 'elle', 'il', 'je', 'la', 'le', 'les', 'on', 'sur', 'tu']:
        return False

    return True

def custom_tokenizer(str):
    return filter(token_filter, map(token_map, str.split(' ')))

def custom_preprocessor(card):
    str = card["name"] + ' ' + card["desc"]
    str = str.lower()

    for separator in ['`', '"', '\t', '\n', '/', '-', ':', '...', ',', ';', '.', '(', ')', '[', ']', '\'', '_', '*', '=', '#']:
        str = str.replace(separator, ' ')

    accentPatterns = {
        'e': ['é', 'è', 'ê'],
        'a': ['à', 'â'],
        'c': ['ç'],
    }

    for pattern in accentPatterns:
        for charToBeReplaced in accentPatterns[pattern]:
            str = str.replace(charToBeReplaced, pattern)

    if card["due"]:
        str += ' _hasDueDate'

    if card["badges"]["attachments"]:
        str += ' _hasAttachment'

    return str

def extractData(data):
    count_vectorizer = CountVectorizer(
        preprocessor=custom_preprocessor,
        tokenizer=custom_tokenizer
    )

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
