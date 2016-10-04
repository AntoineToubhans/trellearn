import sys
import src.importJSON as I
import src.processJSON as P

if __name__ == '__main__':

    print('Hello, I am Trellearn')

    jsonFileName = sys.argv[1]

    cards = I.parseJSON(jsonFileName)

    dataCards = P.extractDataFromCards(cards)

    print('======================================')
    print(dataCards)
    print('======================================')

    exit(0)
