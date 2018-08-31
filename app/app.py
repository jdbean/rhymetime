#!flask/bin/python
import random
from flask import Flask, jsonify, abort, make_response, request

APP = Flask(__name__)

## Custom JSON 404 and 400 errors so that response codes can be processed
## by client
@APP.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@APP.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

## Randomword route for 'post' action.
# get needs to be idempotent for REST so it is inappropriate for
# a random response
@APP.route('/api/v1.0/randomword', methods=['post'])
def random_word():
    # extract JSON if possible and respond 400 otherwise
    request_json = request.get_json()
    # check if the request contains a 'words' key otherwise respond 400
    if 'words' not in request_json:
        abort(400)
    # save word list to a variable
    words_list = request_json['words']
    # check if words_list is actually a list, otherwise respond 400.
    if not isinstance(words_list, list):
        abort(400)
    # check if length of words_list is at least 2, otherwise respond 400.
    if len(words_list) <= 1:
        abort(400)
    # take a random sample from words_list and store in a varible
    random_word_choice = random.choice(words_list)
    # respond with a json payload containing randomly choosen word
    return jsonify({'word': random_word_choice})

if __name__ == '__main__':
    APP.run(debug=True)
