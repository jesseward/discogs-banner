discogs-banner
==============

Creates an image banner from the album thumbnails in your Discogs collection.

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
Modify the configuration values to your needs (see conf/discogs-banner.con)
```
[discogs-banner]
# Required: location to store image thumbnails retrieved from the Discogs
# API. 
cache_directory=/home/jesse/.config/discogs-banner/image-cache

# Required: authorization token file. If this is not present you will be 
# prompted to authenticate with discogs
auth_token=/home/jesse/.config/discogs-banner/token
```

Run the script
```
python discogs-banner.py DISCOGS-USER-NAME-HERE
```
The default settings will drop discogs-banner.jpg in your current working path.

Sample
======
![](https://raw.githubusercontent.com/jesseward/discogs-banner/master/doc/discogs-banner.jpg)
