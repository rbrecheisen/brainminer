import os
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
    
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    username = generate_string(8)
    response = requests.post(uri('/users'), json={
        'username': username, 'password': 'secret', 'email': '{}@me.com'.format(username)}, headers=token_header(token))
    assert response.status_code == 201
    
    response = requests.post(uri('/tokens'), headers=login_header(username, 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    response = requests.post(uri('/users'), json={
        'username': 'bla', 'password': 'secret', 'email': 'bla@me.com'}, headers=token_header(token))
    assert response.status_code == 403


# ----------------------------------------------------------------------------------------------------------------------
def test_upload_and_download_file():

    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']

    response = requests.post(uri('/repositories'), json={'name': generate_string(8)}, headers=token_header(token))
    assert response.status_code == 201
    repository_id = response.json()['id']

    with open('file.txt', 'wb') as f:
        f.write('this is some text')
    with open('file.txt', 'rb') as f:
        response = requests.post(
            uri('/repositories/{}/files'.format(repository_id)), files={'file': f},
            data={'type': 'text', 'modality': 'none'}, headers=token_header(token))
        assert response.status_code == 201
        file_id = response.json()['id']
    os.system('rm file.txt')

    response = requests.get(
        uri('/repositories/{}/files/{}/content'.format(repository_id, file_id)), headers=token_header(token))
    assert response.status_code == 200


if __name__ == '__main__':

    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main(['./brainminer/tests.py', '-s', '-p', 'no:cacheprovider'])
