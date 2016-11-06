from flask import request, g
from jose import jwt, JWTError
from brainminer.auth.dao import UserDao
from brainminer.auth.exceptions import (
    SecretKeyNotFoundException, SecretKeyInvalidException, TokenEncodingFailedException,
    TokenDecodingFailedException, UserNotFoundException, UserNotActiveException, InvalidPasswordException,
    MissingAuthorizationHeaderException)


# ----------------------------------------------------------------------------------------------------------------------
def create_token(user):
    if 'SECRET_KEY' not in g.config.keys():
        raise SecretKeyNotFoundException()
    secret = g.config['SECRET_KEY']
    if secret is None:
        raise SecretKeyInvalidException()
    try:
        token = jwt.encode(user.to_dict(), secret, algorithm='HS256')
        return token
    except JWTError as e:
        raise TokenEncodingFailedException(e.message)


# ----------------------------------------------------------------------------------------------------------------------
def check_jwt_token(token):
    if 'SECRET_KEY' not in g.config.keys():
        raise SecretKeyNotFoundException()
    secret = g.config['SECRET_KEY']
    if secret is None:
        raise SecretKeyInvalidException()
    try:
        data = jwt.decode(token, secret, algorithms=['HS256'])
    except JWTError as e:
        raise TokenDecodingFailedException(e.message)
    user_dao = UserDao(g.db_session)
    user = user_dao.retrieve(id=data['id'])
    if user is None:
        raise UserNotFoundException(id=data['id'])
    if not user.is_active:
        raise UserNotActiveException(id=data['id'])
    return user


# ----------------------------------------------------------------------------------------------------------------------
def check_username_and_password(username, password):
    user_dao = UserDao(g.db_session)
    user = user_dao.retrieve(username=username)
    if user is None:
        raise UserNotFoundException(username=username)
    if not user.is_active:
        raise UserNotActiveException(username=username)
    if user.password != password:
        raise InvalidPasswordException()
    return user


# ----------------------------------------------------------------------------------------------------------------------
def check_login():
    g.current_user = None
    auth = request.authorization
    if auth is None:
        raise MissingAuthorizationHeaderException()
    user = check_username_and_password(auth.username, auth.password)
    g.current_user = user
    return user


# ----------------------------------------------------------------------------------------------------------------------
def check_token():
    g.current_user = None
    auth = request.authorization
    if auth is None:
        raise MissingAuthorizationHeaderException()
    user = check_jwt_token(auth.username)
    g.current_user = user
    return user
