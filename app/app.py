#!flask/bin/python
import random
import re
import pronouncing

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
#
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
    # store word list to a variable
    words_list = request_json['words']
    # check if words_list is actually a list, otherwise respond 400.
    if not isinstance(words_list, list):
        abort(400)
    # check if length of words_list is at least 2, otherwise respond 400
    if len(words_list) <= 1:
        abort(400)
    # take a random sample from words_list and store in a varible
    random_word_chosen = random.choice(words_list)
    # respond with a json payload containing randomly choosen word
    return jsonify({'word': random_word_chosen})

## rhymes route for 'get' action.

@APP.route('/api/v1.0/words/rhymes', methods=['get'])
# Accepts an english word and returns that word along with an array
# of words that rhymes with potential pronounciations of that word.
# Inclusion in the CMU pronouncing dictionary is assumed to be
# necessary and sufficient to classify a string as an 'english word'
def get_rhymes():
    # check if the query string contains a 'query' string and otherwise
    # respond 400
    if 'query' not in request.args:
        abort(400)
    # store value of 'query' key in query to variable
    word = request.args.get('query')
    # store value of regex pattern for any non alpha character
    valid_char_pattern = r'[^A-Za-z\']'
    # check if word non-nil and composed of only valid english-language alpha
    # chars. Regex test is applied her to avoid uneeded dictionary lookup and
    # to distinguish 'Not Found' (404) from 'Bad Request' (400)
    if not word or re.search(valid_char_pattern, word):
        abort(400)
    # Set the value of 'word' to all lowercase
    word = word.lower()
    # Initialize pronouncing's lookup object collection if not yet initialized
    pronouncing.init_cmu()
    # If the word isn't in the CMU pronouncing dictionary respond with 404
    # This is required because the pronouncing library does not offer a
    # distinction between word pronounciation unknown (i.e. rhyme matches
    # unkown) and word found but no rhymes found (i.e. believed to rhyme
    # with no other word in dictionary)
    if not word in pronouncing.lookup:
        abort(404)
    # Use pronouncing to find potential rhymes and store in variable rhymes
    rhymes = pronouncing.rhymes(word)
    # Return json to client with rhymes array and the query
    return jsonify({'ryhmes': rhymes, 'query': word})

if __name__ == '__main__':
    APP.run(debug=True)
