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

## Randomchoice route for 'post' action.
# This route should typically be a GET request. However,
# it has been designated a POST request after some consideration.
# This particular feature is required to accept arguments
# of unspecified length. A GET request's maximum URL will be
# impacted by choice of client and production webserver but could
# be as slow as ~2000 charachters. The choice to use POST here is
# questionable within the REST paradigm but appears to be a common
# choice when confronting the potential of a client request being
# rejected with a 414 error due to excessive length. 
@APP.route('/api/v1.0/words/randomchoice', methods=['post'])
def random_word_choice():
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
