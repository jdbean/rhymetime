import json
import pytest

from rhymetime import APP

# Helper function for decoding JSON data from responses
def response_json(resp):
    return json.loads(resp.data.decode('utf8'))

# Helper function for encoding JSON data for posts
def post_json(client, url, data_obj):
    return client.post(url, data=json.dumps(data_obj),
                       content_type='application/json')

@pytest.fixture
def app():
    app = APP
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_rhyme(client):
    # Basic Test
    response = client.get('/api/v1.0/words/rhymes?word=perfect')
    assert response.status_code == 200
    assert response_json(response)['rhymes'] == ["addict",
                                                "affect",
                                                "becht",
                                                "bedecked",
                                                "benedict",
                                                "brecht",
                                                "checked",
                                                "cmudict",
                                                "collect",
                                                "confect",
                                                "connect",
                                                "correct",
                                                "decked",
                                                "defect",
                                                "deflect",
                                                "deject",
                                                "deregt",
                                                "derelict",
                                                "detect",
                                                "direct",
                                                "disaffect",
                                                "disconnect",
                                                "disinfect",
                                                "disrespect",
                                                "dissect",
                                                "effect",
                                                "eject",
                                                "elect",
                                                "erect",
                                                "expect",
                                                "fecht",
                                                "hecht",
                                                "incorrect",
                                                "indirect",
                                                "infect",
                                                "inject",
                                                "inspect",
                                                "interconnect",
                                                "interdict",
                                                "interject",
                                                "intersect",
                                                "kinect",
                                                "knecht",
                                                "maastricht",
                                                "misdirect",
                                                "necked",
                                                "neglect",
                                                "non-direct",
                                                "nondirect",
                                                "object",
                                                "overprotect",
                                                "pecht",
                                                "precht",
                                                "project",
                                                "protect",
                                                "rechecked",
                                                "recht",
                                                "recollect",
                                                "reconnect",
                                                "redirect",
                                                "reelect",
                                                "reflect",
                                                "reinspect",
                                                "reject",
                                                "respect",
                                                "resurrect",
                                                "schlecht",
                                                "sect",
                                                "select",
                                                "self-respect",
                                                "specht",
                                                "subject",
                                                "suspect",
                                                "teleconnect",
                                                "trekked",
                                                "unchecked",
                                                "wecht",
                                                "wrecked"]
    assert response_json(response)['word'] == "perfect"

    # Test of appropriate non-response to pronunciation_id

    response = client.get('/api/v1.0/words/rhymes?word=perfect&pronunciation_id')
    assert response.status_code == 200
    assert response_json(response)['rhymes'] == ["addict",
                                                "affect",
                                                "becht",
                                                "bedecked",
                                                "benedict",
                                                "brecht",
                                                "checked",
                                                "cmudict",
                                                "collect",
                                                "confect",
                                                "connect",
                                                "correct",
                                                "decked",
                                                "defect",
                                                "deflect",
                                                "deject",
                                                "deregt",
                                                "derelict",
                                                "detect",
                                                "direct",
                                                "disaffect",
                                                "disconnect",
                                                "disinfect",
                                                "disrespect",
                                                "dissect",
                                                "effect",
                                                "eject",
                                                "elect",
                                                "erect",
                                                "expect",
                                                "fecht",
                                                "hecht",
                                                "incorrect",
                                                "indirect",
                                                "infect",
                                                "inject",
                                                "inspect",
                                                "interconnect",
                                                "interdict",
                                                "interject",
                                                "intersect",
                                                "kinect",
                                                "knecht",
                                                "maastricht",
                                                "misdirect",
                                                "necked",
                                                "neglect",
                                                "non-direct",
                                                "nondirect",
                                                "object",
                                                "overprotect",
                                                "pecht",
                                                "precht",
                                                "project",
                                                "protect",
                                                "rechecked",
                                                "recht",
                                                "recollect",
                                                "reconnect",
                                                "redirect",
                                                "reelect",
                                                "reflect",
                                                "reinspect",
                                                "reject",
                                                "respect",
                                                "resurrect",
                                                "schlecht",
                                                "sect",
                                                "select",
                                                "self-respect",
                                                "specht",
                                                "subject",
                                                "suspect",
                                                "teleconnect",
                                                "trekked",
                                                "unchecked",
                                                "wecht",
                                                "wrecked"]
    assert response_json(response)['word'] == "perfect"

    # Test of appropriate response to pronunciation_id of 0

    response = client.get('/api/v1.0/words/rhymes?word=perfect&pronunciation_id=0')
    assert response.status_code == 200
    assert response_json(response)['rhymes'] == ["affect",
                                                "becht",
                                                "bedecked",
                                                "brecht",
                                                "checked",
                                                "collect",
                                                "confect",
                                                "connect",
                                                "correct",
                                                "decked",
                                                "defect",
                                                "deflect",
                                                "deject",
                                                "deregt",
                                                "detect",
                                                "direct",
                                                "disaffect",
                                                "disconnect",
                                                "disinfect",
                                                "disrespect",
                                                "dissect",
                                                "effect",
                                                "eject",
                                                "elect",
                                                "erect",
                                                "expect",
                                                "fecht",
                                                "hecht",
                                                "incorrect",
                                                "indirect",
                                                "infect",
                                                "inject",
                                                "inspect",
                                                "interconnect",
                                                "interject",
                                                "intersect",
                                                "kinect",
                                                "knecht",
                                                "misdirect",
                                                "necked",
                                                "neglect",
                                                "non-direct",
                                                "nondirect",
                                                "object",
                                                "overprotect",
                                                "pecht",
                                                "precht",
                                                "project",
                                                "protect",
                                                "rechecked",
                                                "recht",
                                                "recollect",
                                                "reconnect",
                                                "redirect",
                                                "reelect",
                                                "reflect",
                                                "reinspect",
                                                "reject",
                                                "respect",
                                                "resurrect",
                                                "schlecht",
                                                "sect",
                                                "select",
                                                "self-respect",
                                                "specht",
                                                "subject",
                                                "suspect",
                                                "teleconnect",
                                                "trekked",
                                                "unchecked",
                                                "wecht",
                                                "wrecked"]
    assert response_json(response)['word'] == "perfect"


    # Test of appropriate response to pronunciation_id of 1

    response = client.get('/api/v1.0/words/rhymes?word=perfect&pronunciation_id=1')
    assert response.status_code == 200
    assert response_json(response)['rhymes'] == ["addict",
                                                "benedict",
                                                "cmudict",
                                                "derelict",
                                                "interdict",
                                                "maastricht"]
    assert response_json(response)['word'] == "perfect"

    #no word query argument
    response = client.get('/api/v1.0/words/rhymes')
    assert response.status_code == 400

    #empty string word query argument
    response = client.get('/api/v1.0/words/rhymes?word')
    assert response.status_code == 400

    #word not in dictionary
    response = client.get('/api/v1.0/words/rhymes?word=WubbaLubbaDubDub')
    assert response.status_code == 404

    #invalid charachter
    response = client.get('/api/v1.0/words/rhymes?word=really%3F')
    assert response.status_code == 400

def test_random_word_choice(client):
    # Basic Test
    data = ["Rock", "Paper", "Scissors"]
    response = post_json(client, '/api/v1.0/words/randomchoice',
                        {'words': data})
    assert response.status_code == 200
    assert response_json(response)['word'] in data

    # Single word test
    data = ["Rock"]
    response = post_json(client, '/api/v1.0/words/randomchoice',
                        {'words': data})
    assert response.status_code == 400
    # Empty list test
    data = []
    response = post_json(client, '/api/v1.0/words/randomchoice',
                        {'words': data})
    assert response.status_code == 400
    # Dictionary test
    data = {1: "Rock", 2: "Paper", 3: "Scissors"}
    response = post_json(client, '/api/v1.0/words/randomchoice',
                        {'words': data})
    assert response.status_code == 400

def test_pronunciations(client):
    #basic test
    response = client.get('/api/v1.0/words/pronunciations?word=perfect')
    assert response.status_code == 200
    assert response_json(response)['pronunciations'] == ["P ER0 F EH1 K T",
                                                         "P ER1 F IH2 K T"]
    assert response_json(response)['word'] == "perfect"

    #no word query argument
    response = client.get('/api/v1.0/words/pronunciations')
    assert response.status_code == 400

    #empty string word query argument
    response = client.get('/api/v1.0/words/pronunciations?word')
    assert response.status_code == 400

    #word not in dictionary
    response = client.get('/api/v1.0/words/pronunciations?word=WubbaLubbaDubDub')
    assert response.status_code == 404

    #invalid charachter
    response = client.get('/api/v1.0/words/pronunciations?word=really%3F')
    assert response.status_code == 400
