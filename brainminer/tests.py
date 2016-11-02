import pytest
import requests
from brainminer.base.util import uri, login_header, token_header


# ----------------------------------------------------------------------------------------------------------------------
def test_login():
    response = requests.post(uri('/tokens'), headers=login_header('root', 'secret'))
    assert response.json()['token'] == '1234'


if __name__ == '__main__':
    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main(['./brainminer/tests.py', '-s', '-p', 'no:cacheprovider'])
