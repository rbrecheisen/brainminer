import os
import pytest
import requests
from brainminer.base.util import uri, login_header, token_header, generate_string


# ----------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope='module')
def root_token():
    
    # Create root token
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    token = response.json()['token']
    # This fixture also creates a default user
    response = requests.get(uri('/users?username=user'), headers=token_header(token))
    if len(response.json()) == 0:
        requests.post(uri('/users'), json={
            'username': 'user', 'password': 'secret', 'email': 'user@me.com'}, headers=token_header(token))
    # Return root token
    yield token
    # This code will be executed after the fixture loses scope, i.e., when tests finish. This only
    # works if the previous line 'yields' the result instead of 'returns' it.
    response = requests.get(uri('/users?username=user'), headers=token_header(token))
    if len(response.json()) > 0:
        requests.delete(uri('/users/{}'.format(response.json()[0]['id'])), headers=token_header(token))


# ----------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope='module')
def user_token():
    
    # We're assuming the 'root_token' fixture has already been called and a default 'user'
    # exists in the database.
    response = requests.post(uri('/tokens'), headers=login_header('user', 'secret'))
    return response.json()['token']


# ----------------------------------------------------------------------------------------------------------------------
def test_create_user_already_exists(root_token):

    response = requests.post(uri('/users'), json={
        'username': 'user', 'password': 'secret', 'email': 'bla@me.com'}, headers=token_header(root_token))
    assert response.status_code == 400


# ----------------------------------------------------------------------------------------------------------------------
def test_create_user_with_missing_required_fields(root_token):
    
    username = generate_string(8)
    response = requests.post(uri('/users'), json={'username': username}, headers=token_header(root_token))
    assert response.status_code == 400
    

# ----------------------------------------------------------------------------------------------------------------------
def test_create_user_not_allowed(user_token):

    response = requests.post(uri('/users'), json={
        'username': 'bla', 'password': 'secret', 'email': 'bla@me.com'}, headers=token_header(user_token))
    assert response.status_code == 403
    
    
# ----------------------------------------------------------------------------------------------------------------------
def test_upload_and_download_file(root_token):

    response = requests.post(uri('/repositories'), json={'name': generate_string(8)}, headers=token_header(root_token))
    assert response.status_code == 201
    repository_id = response.json()['id']

    with open('file.txt', 'wb') as f:
        f.write('this is some text')
    with open('file.txt', 'rb') as f:
        response = requests.post(
            uri('/repositories/{}/files'.format(repository_id)), files={'file': f},
            data={'type': 'text', 'modality': 'none'}, headers=token_header(root_token))
        assert response.status_code == 201
        file_id = response.json()['id']
    os.system('rm file.txt')

    response = requests.get(
        uri('/repositories/{}/files/{}/content'.format(repository_id, file_id)), headers=token_header(root_token))
    assert response.status_code == 200
    assert response.content == 'this is some text'
    
    
# ----------------------------------------------------------------------------------------------------------------------
def test_retrieve_file_not_in_repository(root_token):
    pass


# ----------------------------------------------------------------------------------------------------------------------
def test_retrieve_file_set_not_in_repository(root_token):
    pass


# ----------------------------------------------------------------------------------------------------------------------
def test_add_file_to_file_set(root_token):
    pass


# ----------------------------------------------------------------------------------------------------------------------
def test_remove_file_from_file_set(root_token):
    pass


if __name__ == '__main__':

    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main(['./brainminer/tests.py', '-s', '-p', 'no:cacheprovider'])
