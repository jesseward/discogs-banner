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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(args, config):

    
    discogs_collection = fetch_collection(args.user)

    # collection is 0 size . 
    if len(discogs_collection) == 0 :
        logger.error('collection is of 0 length. Exiting.')
        sys.exit(1)

    thumbs = normalize_thumbs(discogs_collection)

    fetch_images('config', thumbs)
    h,v = calculate_canvas(thumbs)

    # send only the image file name to the create method
    create_image(args, [ x[2] for x in thumbs ])
    print h,v

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
        'cache_direcotry': os.path.expanduser('~/.config/discogs-banner/image-cache'),
        'log_file': '/tmp/discogs-banner.log',
        'auth_token': os.path.expanduser('~/.config/discogs-banner/token'),
      })
    config.read(args.c)
    
    m = main(args, config)
