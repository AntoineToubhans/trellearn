import json, os

def parseJSON(fileName):
    print("Parsing JSON File: %s" % fileName)

    filePath = os.path.join('data', fileName)

    with open(filePath, 'r') as file:
        data = json.load(file)

    print("Succesfully imported %d cards from file %s" % (len(data), fileName))

    return data
