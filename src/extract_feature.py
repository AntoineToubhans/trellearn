from sklearn                         import preprocessing
from sklearn.feature_extraction.text import CountVectorizer

def prepareCards(cards):
    preparedCards = {
        'labels': [],
        'data': [],
    }

    for card in cards:
        datum = card["name"] + ' ' + card["desc"]
        for label in card.get("idLabels", []):
            preparedCards["labels"].append(label)
            preparedCards["data"].append(datum)

    return preparedCards

def custom_tokenizer(s):
    return s.split()

def extractData(data):
    count_vectorizer = CountVectorizer(tokenizer=custom_tokenizer)

    return count_vectorizer.fit_transform(data)

def extractLabels(labels):
    label_encoder = preprocessing.LabelEncoder()

    return label_encoder.fit_transform(labels)

def extract(cards):
    print("Preparing %d cards" % len(cards))
    cards = prepareCards(cards)
    print("Extracting features from %d cards" % len(cards["data"]))

    X = extractData(cards["data"])

    y = extractLabels(cards["labels"])

    print("Extraction ok: X %s, y %s" % (X.toarray().shape, y.shape))

    return X, y
