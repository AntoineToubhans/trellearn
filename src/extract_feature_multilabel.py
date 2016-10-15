from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import re

re_phone_number = re.compile(r"(\+33|0)[0-9]{9}$")
re_mongo_id = re.compile(r"(^[0-9a-f]{24}$)|(^[0-9a-f]{12})$")

def prepareCards(cards):
    data, labels = [], []
    for card in cards:
        labels.append(card.pop("idLabels"))
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
        'o': ['ô'],
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

    X = count_vectorizer.fit_transform(data)
    X = TfidfTransformer(use_idf=False).fit_transform(X)

    return X

def extractLabels(labels):
    mlb = MultiLabelBinarizer()

    return mlb.fit_transform(labels)

def extract(cards):
    print("Preparing %d cards" % len(cards))
    data, labels = prepareCards(cards)
    print("Extracting features from %d cards" % len(data))

    X = extractData(data)
    Y = extractLabels(labels)

    print("Extraction ok: X %s, Y %s" % (X.toarray().shape, Y.shape))

    return X, Y
