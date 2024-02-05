import logging
import os
import random

from PIL import Image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

THUMB_WIDTH = 100
THUMB_LENGTH = 100

ASPECT = {
    "16x9": (1.77, 0.56),
    "4x3": (1.33, 0.75),
    "2x1": (2.00, 0.50),
}


def calculate_canvas(thumbs, aspect="16x9"):

    try:
        horizontal = ASPECT[aspect][0]
        vertical = ASPECT[aspect][1]
    except KeyError:
        logger.error(
            "Invalid aspect ratio specified. aspect={ratio}".format(ratio=aspect)
        )
        return (None, None)

    # our total number of pixels
    pixels = THUMB_WIDTH * THUMB_LENGTH * len(thumbs)

    h = (pixels * horizontal) ** (1 / 2.0)
    v = (pixels * vertical) ** (1 / 2.0)

    # trim excess pixels from borders
    return (int(h) - (int(h) % THUMB_WIDTH), int(v) - (int(v) % THUMB_WIDTH))


def normalize_thumbs(thumbs, max_thumbs=119):
    """Set a maximum thumbnail allowance. Goal is to reduce calls
    to the discogs api. This also translates to a maximum of
    1500x1000 image size"""

    # truncate and shuffle our thumbs if the max allowable size is greater
    # than we expect
    if len(thumbs) > max_thumbs:
        logger.info("Truncating thumbs to {max_thumbs}.".format(max_thumbs=max_thumbs))
        random.shuffle(thumbs)
        thumbs = thumbs[:max_thumbs]

    return thumbs


def create_image(config, image_name, thumbs, horizontal=1024, vertical=576):

    # create a blank image canvas
    new_image = Image.new("RGB", (horizontal, vertical))

    # build the image. starting at position 0,0 stepping the thumbnail
    # width on each iteration of the loop
    for i in range(0, horizontal, THUMB_WIDTH):
        for j in range(0, vertical, THUMB_WIDTH):

            try:
                image_file = os.path.basename(thumbs.pop(random.randrange(len(thumbs))))
            except ValueError:
                logger.error("empty list, breaking out of loop.")
                break

            # obtain a random thumbnail image from our list.
            # A missing image will result in a blank 100x100 tile
            try:
                thumb = Image.open(
                    os.path.join(
                        config.get("discogs-banner", "cache_directory"), image_file
                    )
                )
            except IOError:
                logger.error(
                    "Unable to open file {image}, skipping.".format(image=image_file)
                )
                continue
            thumb.thumbnail((THUMB_WIDTH, THUMB_WIDTH), Image.ANTIALIAS)

            # paste the thumb into the image canvas
            new_image.paste(thumb, (i, j))

    new_image.save(image_name, "JPEG")
