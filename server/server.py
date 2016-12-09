import hug
from sklearn.externals import joblib
from src.extract_feature_multilabel import extract, extractData
from src.data_training import train

@hug.post()
def learn(boardId, cards):
    """Learn from board"""
    print("[Learn] %d cards received from board %s !" % (len(cards), boardId))

    X, Y, count_vectorizer, multi_label_binarizer = extract(cards)
    clf = train(X, Y)

    joblib.dump({
        'clf': clf,
        'cv': count_vectorizer,
        'mlb': multi_label_binarizer,
    }, 'data/%s.pkl' % boardId)

    print("Ok ! ---------------> model saved in data/%s.pkl" % boardId)

    return 'OK :)'

@hug.post()
def labels(boardId, card):
    """Return sorted labels"""
    print("[Labels] one card received from board %s !" % boardId)

    ld = joblib.load('data/%s.pkl' % boardId)
    clf = ld['clf']
    mlb = ld['mlb']
    cv = ld['cv']

    X = cv.transform([card])

    def format(t):
        x, y = t
        return {
            'p': x,
            'id': y,
        }

    return sorted(
        map(format, zip(clf.predict_proba(X)[0], mlb.classes_)),
        key=lambda t: -t['p']
    )

@hug.response_middleware()
def process_data(request, response, resource):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
#    response.set_header('Content-Type', 'application/json; charset=utf-8')
#    response.set_header('Content-Type', '*')
