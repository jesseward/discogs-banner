import logging
import os
import shutil
import time

import requests

from discogs_banner.discogs_wrapper import DiscogsWrapper

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)


def fetch_images(config, images):
    """
    Downloads and persists discogs thumbnail images to local disk.

    :param config: ConfigParser object
    :param images: List containing release id, release title and release
                   thumbnail.
    """

    logger = logging.getLogger(__name__)

    for image in images:

        image_file_name = os.path.join(
            config.get("discogs-banner", "cache_directory"), os.path.basename(image[2])
        )

        # if the file exists, do not overwrite and do not download
        if os.path.isfile(image_file_name):
            logger.info(
                "skipping file={file_name}, already exists in cache.".format(
                    file_name=image_file_name
                )
            )
            continue

        # limit to 1 QPS to discogs API.
        time.sleep(1)

        response = requests.get(image[2], stream=True)
        if response.status_code == 200:
            logger.debug(
                "Downloaded image. release-id={release},url={url}".format(
                    release=image[0], url=image[2]
                )
            )

            with open(image_file_name, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

        else:
            logger.error(
                "error response. http status code={code}, url={url}".format(
                    code=response["status"], url=image[2]
                )
            )


def fetch_collection(config, user):
    """
    Fetches a json object representing a users collection.

    :param user: str representing a discogs user name
    :return: a list containing release id, release title and release thumbnail
    """

    logger = logging.getLogger(__name__)
    max = 100
    count = 0
    collection = []

    dw = DiscogsWrapper(config)
    discogs_user = dw.discogs.user(user)

    # ensure the taret user has a valid collections folder and this
    # collection has at least 20 releases, otherwise creating the banner isn't
    # worthwhile..
    if (
        len(discogs_user.collection_folders) == 0
        or len(discogs_user.collection_folders[0].releases) < 20
    ):
        logger.error("User does not have a large enough collection")
        raise LookupError

    for rel in discogs_user.collection_folders[0].releases:

        rel_id = rel.release.id
        rel_title = rel.release.title
        rel_thumb = rel.release.thumb

        # ignore default "spacer" images, or an empty string..
        if rel_thumb in ("spacer.gif", ""):
            logger.warn(
                "Ignoring {release} ({rid}) due to an empty thumbnail image".format(
                    release=rel_title, rid=rel_id
                )
            )
            continue

        # create a list datastructure for our results.
        try:
            logger.debug(
                "Adding {id}->{title}->{thumb} as targets.".format(
                    id=rel_id, title=rel_title, thumb=rel_thumb
                )
            )
            collection.append([rel_id, rel_title, rel_thumb])
        except requests.exceptions.SSLError as xxx_todo_changeme:
            requests.exceptions.ConnectionError = xxx_todo_changeme
            logger.error("Fetch Error at {rid}, skipping.".format(rid=rel))
            continue
        if count == max:
            break

        count += 1

        # attempt to avoid rate limiting by discogs.
        time.sleep(1)
    return collection
