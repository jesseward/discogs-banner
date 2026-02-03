discogs-banner
==============

Creates an image banner from the album thumbnails in your Discogs collection.

Note that Discogs imposes a rate and request limit on their image request API. Calls to fetch an image require your request to be wrapped in OAuth1.0. I have included a key and secret in this script to get things running quickly. Though you should request your own from the discogs site, to ensure you're not sharing your quota against the key-pair provided here. If you receive errors while fetching images (HTTP error 403), you've likely reached the 1000 per day limit.

Install
=======

Clone repo from github
```
git clone https://github.com/jesseward/discogs-banner.git
cd discogs-banner
```

Use the included Makefile to set up the environment:

```bash
make venv
```

This will create a virtual environment in `.venv` and install all necessary dependencies.

How
===
1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. **Configuration:**

   **Environment Variables (Recommended):**
   Set your Discogs API keys as environment variables:
   ```bash
   export DISCOGS_CONSUMER_KEY='your_consumer_key'
   export DISCOGS_CONSUMER_SECRET='your_consumer_secret'
   ```

   **Configuration File:**
   Modify the configuration values to your needs (see `config/discogs-banner.conf`):

   ```ini
   [discogs-banner]
   # Required: location to store image thumbnails retrieved from the Discogs API. 
   cache_directory=/home/YOUR_USER/.config/discogs-banner/image-cache

   # Required: authorization token file. If this is not present you will be 
   # prompted to authenticate with discogs
   auth_token=/home/YOUR_USER/.config/discogs-banner/token
   ```

   **Note:** You may want to create your own Discogs API keys at [https://www.discogs.com/developers/](https://www.discogs.com/developers/) to avoid shared rate limits.

3. Run the script:
   ```bash
   python scripts/discogs-banner.py DISCOGS-USER-NAME-HERE
   ```
   
   The default settings will drop a 16x9 `discogs-banner.jpg` in your current working path.

Development
===========

Use the Makefile for common tasks:

*   **Format code:** `make format` (uses `black`)
*   **Run tests:** `make test`
*   **Clean environment:** `make clean`

Run-time command line options.
```
$ python scripts/discogs-banner.py --help
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
