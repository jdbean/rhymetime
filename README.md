# Introduction

{**REMOVED**}

# Assignment

{**REMOVED**}

# Description

This tool implements a restful JSON API at /api/v1.0/words/
with three routes:

## POST randomchoice

The `randomchoice` route accepts a JSON object containg a `words`
key with a value of a list containing two or more elements. The route
returns a JSON object with a key of 1`word` and a value of one of
the submitted elements selected at random.

This route opts for the use of POST over GET in order to be able
to more reliably support lengthy submissions

## GET pronunciations

The `pronunciations` route accepts a query with a `word` argument of one
english word and returns a json object containing a `pronunciations` and a
`word` key. The `pronunciations` key contains a list of the known possible
pronunciations of that word using ARPAbet[^1] notation. `word` contains
the queried word.

Words are considered english only if they appear in the CMU Pronouncing
Dictionary.

## GET rhymes

The `rhymes` route accepts a query with a `word` argument of one
english word and optionally a `pronunciation_id` route corresponding
to the index of the pronunciation returned from `GET pronunciations`.
The route returns a JSON object with a `rhymes` and `word` key. The
`word` key always contains the queried word. If no optional parameter
is provided by the client, the `rhymes` key will contain a list of
all rhymes detected in the CMU pronouncing dictionary for all known
pronunciations of the queried word or, in the event that no rhymes
are found in dictionary, an empty list. If a valid pronunciation
index id if provided, the `rhymes` key will contain a list of only
those words that rhyme with the particular pronunciation.

`GET pronunciations` and `GET rhymes` are intended to be used together
to provide a more advanced search feature than `GET rhymes` alone.


# Dependencies/Environment

* Python 3.5
* pip 9.0.1
* wheel*
* venv 3.5*


\*: Not required but recommended

# Basic Install (Debian/Ubuntu/Mint Linux)

1. Install python 3.5
1. Unpack/Clone this repo
1. Open a Terminal in the root directory of this project
1. (Optionally) Create a virtual environment (`venv`) and activate it by running:

    `$ source ./venv/bin/activate`

1. Install pip and wheel (if not already installed)
1. Install dependencies listed in `requirements.txt` by executing:

    `$ pip install -r ./requirements.txt`

1. Set the Flask environment variable:

    `$ export FLASK_APP=rhymetime`

1. Execute:

    `$ flask run`


Alternatively, you may use the included `dockerfile` to create
a docker image/container.


# Tests

Tests have been created for this project and are located in the `/tests`
directory. in order to run the tests execute `pytest` or, for more
details `pytest -v`.

[^1]: https://en.wikipedia.org/wiki/ARPABET
