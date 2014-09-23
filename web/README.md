what
====

The 'web' components of discogs-banner provide a simple flask based API and minimal javascript based front end that allows users to create a discogs collage via the web.

running
=======

start the wsgi engine.
```
uwsgi --ini conf/uwsgi.conf
```

launch the celery worker
```
celery -A tasks worker --loglevel=info
```

Ensure redis is installed and running.

configuration
=============
conf/uwsgi.conf
conf/discogs-collage.housejunkie.ca.conf
conf/api.discogs-collage.housejunkie.ca.conf
