import os
import time
import base64
import string
import random

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


# ----------------------------------------------------------------------------------------------------------------------
def uri(path):
    host = os.getenv('BRAINMINER_HOST', '0.0.0.0')
    port = os.getenv('BRAINMINER_PORT', '5000')
    port = int(port)
    if path.endswith('/'):
        path = path[:-1]
    if path.startswith('/'):
        path = path[1:]
    return 'http://{}:{}/{}'.format(host, port, path)


# ----------------------------------------------------------------------------------------------------------------------
def encode(username, password='unused'):
    return base64.b64encode('{}:{}'.format(username, password))


# ----------------------------------------------------------------------------------------------------------------------
def login_header(username, password):
    return {'Authorization': 'Basic {}'.format(encode(username, password))}


# ----------------------------------------------------------------------------------------------------------------------
def token_header(token):
    return {'Authorization': 'Basic {}'.format(encode(token))}


# ----------------------------------------------------------------------------------------------------------------------
def timing_now():
    return time.time()


# ----------------------------------------------------------------------------------------------------------------------
def timing_elapsed_to_str(start):
    nr_hours, nr_minutes, nr_seconds = timing_elapsed(start)
    nr_hours = '0' + str(nr_hours) if nr_hours < 10 else str(nr_hours)
    nr_minutes = '0' + str(nr_minutes) if nr_minutes < 10 else str(nr_minutes)
    nr_seconds = '0' + str(nr_seconds) if nr_seconds < 10 else str(nr_seconds)
    return '{}:{}:{}'.format(nr_hours, nr_minutes, nr_seconds)


# ----------------------------------------------------------------------------------------------------------------------
def timing_elapsed(start):
    delta = timing_now() - start
    nr_hours = int(delta / 3600)
    nr_minutes = int((delta - nr_hours * 3600) / 60)
    nr_seconds = int((delta - nr_hours * 3600 - nr_minutes * 60))
    return nr_hours, nr_minutes, nr_seconds


# ----------------------------------------------------------------------------------------------------------------------
def date_to_str(date):
    return '{}-{}-{}'.format(date.day, date.month, date.year)


# ----------------------------------------------------------------------------------------------------------------------
def datetime_to_str(datetime):
    return datetime.strftime('%d-%m-%Y %H:%M:%S.%f')


# ----------------------------------------------------------------------------------------------------------------------
def generate_id(n=16):
    if n <= 8:
        return ''.join(random.sample(string.digits, n))
    k = int(n / 8)
    r = n - 8 * k
    nr = ''
    for i in range(k):
        nr += ''.join(random.sample(string.digits, 8))
    nr += ''.join(random.sample(string.digits, r))
    return nr


# ----------------------------------------------------------------------------------------------------------------------
def generate_string(n=64):
    cutoff = 32
    if n <= cutoff:
        text = ''.join(random.sample(string.lowercase + string.digits, n))
        text = random.sample(string.lowercase, 1)[0] + text[1:]
        return text
    k = int(n / cutoff)
    r = n - cutoff * k
    text = ''
    for i in range(k):
        text += ''.join(random.sample(string.lowercase + string.digits, cutoff))
    if r > 0:
        text += ''.join(random.sample(string.lowercase + string.digits, r - 1))
    text = random.sample(string.lowercase, 1)[0] + text[1:]
    return text


# ----------------------------------------------------------------------------------------------------------------------
def get_x(features):
    predictors = list(features.columns)
    x = features[predictors]
    x = x.as_matrix()
    return x


# ----------------------------------------------------------------------------------------------------------------------
def get_xy(features, target_column=None, exclude_columns=list()):
    predictors = list(features.columns)
    for column in exclude_columns:
        if column in predictors:
            predictors.remove(column)
    if target_column:
        if not target_column in exclude_columns:
            if target_column in predictors:
                predictors.remove(target_column)
    x = features[predictors]
    x = x.as_matrix()
    if target_column:
        y = features[target_column]
        y = y.as_matrix()
    else:
        y = None
    return x, y


# ----------------------------------------------------------------------------------------------------------------------
def score_svm(x, y, train=None, test=None):

    param_grid = [{
        'C':     [2**k for k in range(-5, 15, 2)],
        'gamma': [2**k for k in range(-15, 4, 2)]}]

    classifier = GridSearchCV(SVC(kernel='rbf'), param_grid=param_grid, scoring='accuracy')

    score = 0
    if train is not None:
        classifier.fit(x[train], y[train])
        score = classifier.score(x[test], y[test])
        print('Accuracy: {}'.format(score))
    else:
        classifier.fit(x, y)

    return classifier, score


# ----------------------------------------------------------------------------------------------------------------------
def train_svm(x, y):

    classifier, score = score_svm(x, y)
    return classifier
