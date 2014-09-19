import re
import logging

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
