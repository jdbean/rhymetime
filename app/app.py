#!flask/bin/python
from itertools import chain
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

# Helper function for attempting to convert a string to an integer
def try_int(string):
    try:
        integer = int(string)
        return integer
    except ValueError:
        return False
# Helper function to find all rhymes for all known pronunciations of a word
# Achieves advertised functionality of pronouncing.rhymes() at
# https://pronouncing.readthedocs.io/en/latest/tutorial.html#rhyme
# Docs state that function will return rhymes for all possible pronunciations
# As written, function returns rhymes only for the first pronunciation.
#
# NOTE: THIS FUNCTION IS BASED ON CODE FROM PRONOUNCING
# `pronouncingpy/pronouncing/__init__.py` line 203
# issue: https://github.com/aparrish/pronouncingpy/issues/45
# pull-request: https://github.com/aparrish/pronouncingpy/pull/46
def all_rhymes(word):
    # find list of all pronunciations for word
    phones = pronouncing.phones_for_word(word)
    # setup empty list to hold matching rhyme array for mutliple
    # pronunciations
    combined_rhymes = []
    if phones:
        # add the lists of rhyming words for each pronunciation to new list.
        for element in phones:
            combined_rhymes.append([w for w in pronouncing.rhyme_lookup.get(
                                   pronouncing.rhyming_part(element), [])
                                   if w != word])
        # flatten list of lists
        combined_rhymes = list(chain.from_iterable(combined_rhymes))
        # sort the new combined list
        combined_rhymes.sort()
        return combined_rhymes
    else:
        return []

def validate_english_word(args):
    # store value of 'word' key in query to variable
    word = args.get('word')
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
    # distinction between word pronunciation unknown (i.e. rhyme matches
    # unkown) and word found but no rhymes found (i.e. believed to rhyme
    # with no other word in dictionary)
    if not word in pronouncing.lookup:
        abort(404)
    return word

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
# of words that rhymes with potential pronunciations of that word.
# Inclusion in the CMU pronouncing dictionary is assumed to be
# necessary and sufficient to classify a string as an 'english word'
def get_rhymes():
    # Validate the requested english word and if return, store word in variable
    word = validate_english_word(request.args)
    # Use pronouncing to find potential rhymes and store in variable rhymes
    pronounce_str = request.args.get('pronunciation_id')

    if pronounce_str:
        # Assign pronounce to return of try_int() [int or false]
        pronounce_id = try_int(pronounce_str)
        # find list of all pronunciations for word
        pronunciations = pronouncing.phones_for_word(word)
        # if pronounce_id is not an int respond 400 (conversion failed)
        if not isinstance(pronounce_id, int):
            abort(400)
        # is pronounce_id a valid pronunciation index. Return 404 if not
        if pronounce_id not in range(len(pronunciations)):
            abort(404)
        # identify the portion of specified pronunciation relevant to rhyming
        rhyme_sound = pronouncing.rhyming_part(pronunciations[pronounce_id])
        # store list of rhyming words
        rhymes = pronouncing.search(rhyme_sound + "$")
    else:
        # if no pronunciation_id is provided by user, store list of rhymes for
        # all pronunciatons of the word
        rhymes = all_rhymes(word)
    # Return json to client with rhymes array and the queried word
    return jsonify({'rhymes': rhymes, 'word': word})



@APP.route('/api/v1.0/words/pronunciations', methods=['get'])
def get_pronunciations():
    # Validate the requested english word and if return, store word in variable
    word = validate_english_word(request.args)
    # find list of all pronunciations for word
    pronunciations = pronouncing.phones_for_word(word)
    # return list pronunciation phones and the queried word to user
    return jsonify({'pronunciations': pronunciations, 'word': word})

if __name__ == '__main__':
    APP.run(debug=True)
