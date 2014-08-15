discogs-banner
==============

Creates an image banner from the album thumbnails in your Discogs collection.

Note that Discogs imposes a rate and request limit on their image request API. Calls to fetch an image require your request to be wrapped in OAuth1.0. I have included a key and secret in this script to get things running quickly. Though you should request your own from the discogs site, to ensure you're not sharing your quota against the key-pair provided here. If you receive errors while fetching images (HTTP error 403), you've likely reached the 1000 per day limit.

Install
=======

Clone repo from github
```
git clone https://github.com/jesseward/discogs-banner.git
```

Install deps
```
cd discogs-banner
virtualenv ~/.virtualenvs/discogs-banner
source ~/.virtualenvs/discogs-banner/bin/activate
pip install -r requirements.txt # note PIL may be present in your distros packaging system##
python setup.py install
```

How
===
Modify the configuration values to your needs (see conf/discogs-banner.conf)
```
[discogs-banner]
# Required: location to store image thumbnails retrieved from the Discogs
# API. 
cache_directory=/home/jesse/.config/discogs-banner/image-cache

# Required: authorization token file. If this is not present you will be 
# prompted to authenticate with discogs
auth_token=/home/jesse/.config/discogs-banner/token
```
API key data.
```
[discogs-auth]
# Required: Discogs API keys provided to developers. Note that the API
# limits to 1000 requests per day. You should apply for your own keypair
# or else you may risk reaching API limitations (HTTP ERROR 403)
# See : https://www.discogs.com/developers/
consumer_key=ksVetEMWkfaVmiJYlcPx
consumer_secret=TxceKmGYDoTshimvywXmxJoEIffgVzgr
```

Run the script
```
python discogs-banner.py DISCOGS-USER-NAME-HERE
```
The default settings will drop a 16x9 discogs-banner.jpg in your current working path.

Run-time command line options.
```
$ discogs-banner.py --help
usage: discogs-banner.py [-h] [-r R] [-o O] [-c C] user

Create image banner from Discogs album thumbs. Requires your Discogs
collection to be populated (and public)

positional arguments:
  user        Target Discogs account name

optional arguments:
  -h, --help  show this help message and exit
  -r R        Aspect ratio for output image. Options are: 16x9, 2x1, 4x3
  -o O        Output filename for rendered image.
  -c C        Specify an optional configuration file path.

```

Sample
======
![](https://raw.githubusercontent.com/jesseward/discogs-banner/master/doc/discogs-banner.jpg)
