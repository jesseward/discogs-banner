# -*- coding: utf-8 -*-
import re
from datetime import timedelta
from functools import update_wrapper
import logging
from flask import make_response, request, current_app

logger = logging.getLogger(__name__)

def is_valid_username(username):
    ''' ensures user input matches the discogs username specification.
        Allowed characters: letters, numbers, underscore (_), hyphen (-), 
        and period (.)

        :param username: discogs username
        :type username: string

        :return: returns a cleaned username to the caller
        :rtype: string or None if username does not validate. '''

    VALID = r'([A-Za-z0-9\-\_\.]+)'

    match = re.match(VALID, username)

    if match:
        logger.debug('user_id={user_id} is valid'.format(user_id=username))
        return match.group(1)

    logger.warn('user_id={user_id} is not a valid format'.format(user_id=username))



def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
