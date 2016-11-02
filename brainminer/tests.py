import pytest
import requests
from brainminer.base.util import uri, login_header, token_header, generate_string


# ----------------------------------------------------------------------------------------------------------------------
def test_login():
    
    response = requests.post(uri('/tokens'), headers=login_header(generate_string(8), 'secret'))
    assert response.status_code == 403
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.status_code == 201
    
    
# ----------------------------------------------------------------------------------------------------------------------
def test_create_user_missing_required_fields():
    
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    username = generate_string(8)
    response = requests.post(uri('/users'), json={'username': username}, headers=token_header(token))
    assert response.status_code == 400
    

# ----------------------------------------------------------------------------------------------------------------------
def test_create_user():
    
    # Root user creates user
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    username = generate_string(8)
    response = requests.post(uri('/users'), json={
        'username': username, 'password': 'secret', 'email': '{}@me.com'.format(username)}, headers=token_header(token))
    assert response.status_code == 201
    
    # Newly created user tries to create user of his own (should fail)
    response = requests.post(uri('/tokens'), headers=login_header(username, 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    response = requests.post(uri('/users'), json={
        'username': 'bla', 'password': 'secret', 'email': 'bla@me.com'}, headers=token_header(token))
    assert response.status_code == 403


if __name__ == '__main__':
    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main(['./brainminer/tests.py', '-s', '-p', 'no:cacheprovider'])
