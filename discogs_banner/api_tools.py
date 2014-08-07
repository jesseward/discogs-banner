import urllib2
import json
import logging
import time
import os

from discogs_banner.discogs_auth import DiscogsAuth

COLLECTION_BASE = 'http://api.discogs.com/users/{user}/collection/folders/0/releases?page={page}&per_page={count}'
USER_AGENT = 'discogs-banner'


def fetch_images(config, images):

    logger = logging.getLogger(__name__)
    discogs_auth = DiscogsAuth()

    for image in images:

        image_file_name = os.path.join('/home/jesse/scratch',
                os.path.basename(image[2]))
        time.sleep(1)

        resp, content = discogs_auth.handle.request(image[2], 'POST',
            headers={'user-agent': USER_AGENT })

        if resp['status'] == '200':

            if os.path.isfile(image_file_name):
                logger.info('skipping file={file_name}, already exists in cache.'.format(
                    file_name=image_file_name))
                continue

            logger.debug('Downloading image. release-id={release},url={url}'.format(
            release=image[0], url=image[2]))
            with open(image_file_name, 'w') as file_handle:
                file_handle.write(content)
        else:
            logger.error('error response from API. http status code={code}'.format(
                code=resp['status']))


def fetch_collection(user):
    ''' Fetches a json object representing a users collection. '''

    logger = logging.getLogger(__name__)
    next_page = True
    page = 1
    count = 100
    url = COLLECTION_BASE.format(user=user, page=page, count=count)
    collection = []

    while next_page is True:
        try:
            logger.info('fetching url={url}'.format(url=url))
            req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
            response = json.loads(urllib2.urlopen(req).read())
        except urllib2.URLError, e:
            next_page = False
            logger.error('failed to fetch url={url}'.format(url=url))
            continue

        try:
            url = response['pagination']['urls']['next']
        except KeyError:
            next_page = False

        for release in response['releases']:

            # ignore default "spacer" images.
            if 'spacer.gif' in release['basic_information']['thumb']: continue

            collection.append(
                    [release['basic_information']['id'], 
                        release['basic_information']['resource_url'],
                        release['basic_information']['thumb'] ]
            )

    return collection
