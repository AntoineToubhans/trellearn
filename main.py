import sys
import src.importJSON as I
import src.processJSON as P

if __name__ == '__main__':

    print('Hello, I am Trellearn')

    jsonFileName = sys.argv[1]

    json = I.parseJSON(jsonFileName)

    result = P.naiveBayesRegression(json)

    print('======================================')
    print(result)
    print('======================================')

    exit(0)
