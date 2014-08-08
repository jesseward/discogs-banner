#!/usr/bin/env python
import os
import sys
import argparse
import logging
import ConfigParser

from discogs_banner.api_tools import fetch_collection, fetch_images
from discogs_banner.canvas_tools import (
        normalize_thumbs,
        calculate_canvas,
        create_image,
)

def main(args, config):

    
    discogs_collection = fetch_collection(args.user)

    # collection is 0 size . 
    if len(discogs_collection) == 0 :
        logger.error('collection is of 0 length. Exiting.')
        sys.exit(1)

    thumbs = normalize_thumbs(discogs_collection)

    fetch_images(config, thumbs)
    h,v = calculate_canvas(thumbs)

    # send only the image file name to the create method
    logger.info('Creating image={image}, at {h}x{v}'.format(
        image=args.o, h=h, v=v)) 
    create_image(config, args.o, [ x[2] for x in thumbs ])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create image banner from Discogs album thumbs. Requires your Discogs collection to be populated (and public)')
    parser.add_argument('user', type=str, help='Target Discogs account name')
    parser.add_argument('-o', default='discogs-banner.jpg',
        help='Output filename for rendered image.')
    parser.add_argument('-c', default=
            os.path.expanduser('~/.config/discogs-banner/discogs-banner.conf'),
        help='Specify an optional configuration file path.')

    args = parser.parse_args()

    if not os.path.exists(args.c):
        print 'Exiting, unable to locate config file {0}. use -c to specify config target'.format(
            args.c)
        sys.exit(1)

    # apply defaults to *required* configuration values.
    config = ConfigParser.ConfigParser(defaults = {
        'cache_directory': os.path.expanduser('~/.config/discogs-banner/image-cache'),
        'log_file': os.path.expanduser('~/.config/discogs-banner/discogs-banner.log'),
        'auth_token': os.path.expanduser('~/.config/discogs-banner/token'),
      })

    config.read(args.c)

    FORMAT = '%(asctime)-15s [%(process)d] [%(name)s %(funcName)s] [%(levelname)s] %(message)s'
    logging.basicConfig(filename=config.get('discogs-banner',
      'log_file'), format=FORMAT, level=logging.ERROR)
    logger = logging.getLogger('main')

    if not os.path.exists(config.get('discogs-banner', 'cache_directory')):
        logger.warn('Cache directory not found. Creating {cache_dir}'.format(
            cache_dir=config.get('discogs-banner', 'cache_directory')))
        os.mkdir(config.get('discogs-banner', 'cache_directory'))
    
    m = main(args, config)
