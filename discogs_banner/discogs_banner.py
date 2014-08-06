import os
import sys
import random
import itertools
import argparse
from os import listdir
from os.path import isfile, join
from PIL import Image
import logging

from discogs_banner.discogs_collection import fetch_collection, fetch_images


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

THUMB_WIDTH = 100
THUMB_LENGTH = 100

def calculate_canvas(thumbs):

    # default to a 2:1 image ratio
    horizontal = 2.0
    vertical = 0.50
    # our total number of pixels
    pixels = THUMB_WIDTH*THUMB_LENGTH*len(thumbs)

    h = (pixels * horizontal) ** (1/2.0)
    v = (pixels * vertical) ** (1/2.0)

    # trim excess pixels from borders
    return (int(h) - (int(h)%THUMB_WIDTH), int(v) - (int(v)%THUMB_WIDTH))

def normalize_thumbs(thumbs, max_thumbs=119):
    ''' Set a maximum thumbnail allowance. Goal is to reduce calls
        to the discogs api. This also translates to a maximum of 
        1500x1000 image size'''

    # truncate and shuffle our thumbs if the max allowable size is greater
    # than we expect
    if len(thumbs) > max_thumbs:
        logger.info('Truncating thumbs to {max_thumbs}.'.format(
                max_thumbs=max_thumbs))
        random.shuffle(thumbs)
        thumbs = thumbs[:max_thumbs]

    return thumbs

def create(args, thumbs):

    horizontal, vertical = calculate_canvas(thumbs)
    # create a blank image canvas
    new_image = Image.new('RGB', (horizontal, vertical))
   
    # build the image. starting at position 0,0 stepping the thumbnail
    # width on each iteration of the loop
    for i in xrange(0, horizontal, THUMB_WIDTH):
        for j in xrange(0, vertical, THUMB_WIDTH):

            try:
                image_file = os.path.basename(
                        thumbs.pop(random.randrange(len(thumbs))))
            except ValueError:
                logger.error('empty list, breaking out of loop.')
                break

            # obtain a random thumbnail image from our list.
            # A missing image will result in a blank 100x100 tile
            try:
                thumb = Image.open(
                    os.path.join(
                        '/home/jesse/scratch/', image_file)
                )
            except IOError:
                logger.error('Unable to open file {image}'.format(image=
                    image_file))
                continue
            thumb.thumbnail((THUMB_WIDTH, THUMB_WIDTH), Image.ANTIALIAS)

            # paste the thumb into the image canvas
            new_image.paste(thumb, (i, j))

    new_image.save(args.o, "JPEG")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Discogs image banner.')
    parser.add_argument('user', type=str)
    parser.add_argument('-o', default='disogs-banner.jpg')

    args = parser.parse_args()

    coll = fetch_collection(args.user)

    # collection is 0 size . 
    if len(coll) == 0 : sys.exit('bail')

    thumbs = normalize_thumbs(coll)
    print len(thumbs)
    fetch_images('config', thumbs)
    h,v = calculate_canvas(thumbs)
    # send on;ly the image file name to the create method
    create(args, [ x[2] for x in thumbs ])
    print h,v

