import os
import logging
from celery import Celery
import ConfigParser
 
from discogs_banner.canvas_tools import (
        normalize_thumbs,
        calculate_canvas,
        create_image
    )
from discogs_banner.api_tools import fetch_images, fetch_collection


celery = Celery('tasks')
celery.config_from_object('celeryconfig')

logger = logging.getLogger(__name__)

@celery.task(name='tasks.fetch_and_generate')
def fetch_and_generate(username, config):
    ''' Long running task that implements the discogs-banner module. Calls to
        fetch the album art as well as generating the banner/collage.

        :param username: discogs username
        :type username: string

        :param config: configuration options.
        :type config: Config Object

        :return: returns a bool type based on job state.
        :rtype: boolean '''

    # TODO: actually pull from a configuration file.
    config = ConfigParser.ConfigParser()
    config.add_section('discogs-banner')
    config.set('discogs-banner', 'cache_directory', os.path.expanduser('~/.config/discogs-banner/image-cache'))
    config.set('discogs-banner', 'log_file', os.path.expanduser('~/.config/discogs-banner/discogs-banner.log'))
    config.set('discogs-banner', 'auth_token', os.path.expanduser('~/.config/discogs-banner/token'))
    config.add_section('discogs-auth')
    config.set('discogs-auth', 'consumer_key', '')
    config.set('discogs-auth', 'consumer_secret', '')
    discogs_collection = fetch_collection(username)

    if len(discogs_collection) == 0 :
        logger.error('username={username} collection is 0 size'.format(
            username=username))
        return False

    thumbs = normalize_thumbs(discogs_collection)

    fetch_images(config, thumbs)
    h,v = calculate_canvas(thumbs, aspect='16x9')

    if not h or not v:
        logger.error('unable to cacluate image canvas size.')
        return False

    create_image(config, username, [ x[2] for x in thumbs ],
            horizontal=h, vertical=v)

    return True
