import json
from flask import Flask, jsonify, request

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

app = Flask(__name__)

# load config from a JSON file (or anything outputting a python dictionary)
config = {
    "database": {
        "host": "db",
        "user": "postgres",
        "password": "password",
        "database": "dejavu"
    },
    "database_type": "postgres"
}

# create a Dejavu instance
djv = Dejavu(config)

@app.route('/recognize', methods = ['POST'])
def recognize():
    if (request.method == 'POST'):
        file = request.files['file']
        file.save(file.filename)
        results = djv.recognize(FileRecognizer, file.filename)
        
        for result in results['results']:
            result['song_name'] = result['song_name'].decode('utf-8')
            result['file_sha1'] = result['file_sha1'].decode('utf-8')
            result['input_total_hashes'] = int(result['input_total_hashes'])
            result['fingerprinted_hashes_in_db'] = int(result['fingerprinted_hashes_in_db'])
            result['hashes_matched_in_input'] = int(result['hashes_matched_in_input'])
            result['offset'] = int(result['offset'])

        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)

