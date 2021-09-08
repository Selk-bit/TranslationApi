from flask import *
from Translator import Deepl
from difflib import SequenceMatcher



app = Flask(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route('/', methods=['POST'])
def home():
    arr = [
        "Bulgarian",
        "Chinese",
        "Czech",
        "Danish",
        "Dutch",
        "English",
        "Estonian",
        "Finnish",
        "French",
        "German",
        "Greek",
        "Hungarian",
        "Italian",
        "Japanese",
        "Latvian",
        "Lithuanian",
        "Polish",
        "Portuguese",
        "Romanian",
        "Russian",
        "Slovak",
        "Slovenian",
        "Spanish",
        "Swedish",
    ]
    myJson = request.json
    source = myJson["source"]
    dest = myJson["dest"]
    text = myJson["text"]
    count = 0
    for lan in arr:
        if similar(source, lan) > 0.8:
            break
        else:
            count += 1
    if count == len(arr):
        return 'The Source Language is not Supported'
    else:
        count = 0

    for lan in arr:
        if similar(dest, lan) > 0.8:
            break
        else:
            count += 1
    if count == len(arr):
        return 'The Destination Language is not Supported'

    translated = Deepl(source, dest, text)
    return translated

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)