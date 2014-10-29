import json
from os import path, environ
from flask import Flask, Response, abort, request, session
from celery.result import AsyncResult
import logging

from utils import is_valid_username, crossdomain
from tasks import fetch_and_generate

app = Flask(__name__)
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class Result(object):
    ''' utility class to build a json object containing the error or success states
        of the given query. '''

    def __init__(self, user_id):
        self.user_id = user_id
        self.error = None
        self.result = None
        self.job_id = 'UNKNOWN'
        self.mimetype = 'application/json'

    @property
    def render(self):
        res = {}
        res['job_id'] = self.job_id
        res['user_id'] = self.user_id
        res['error'] = self.error
        res['result'] = self.result
        return json.dumps(res)


@app.route("/api/v1/create/<user_id>/", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def api_create_collage(user_id):
    ''' end-point that kicks off the collage creation process. A user_id is received, which
        if valid a celery job is created to perform the long running task.

        :param user_id: discogs username
        :type username: string

        :return: returns a Result object to the caller
        :rtype: Result '''

    res = Result(user_id)
    logger.debug('Received create request for user_id={user_id}'.format(user_id=
        user_id))
    username = is_valid_username(user_id)

    if not username:
        res.error = 'Invalid discogs.com username.'
        return Response(res.render, res.mimetype)

    result = fetch_and_generate.apply_async((user_id, 'TODO:fake_config_here'))
    res.job_id = result.task_id

    return Response(res.render, res.mimetype)

@app.route("/api/v1/status/<user_id>/<task_id>")
@crossdomain(origin='*')
def api_check_status(user_id, task_id, methods=['GET', 'OPTIONS']):
    ''' polls the celery queue given the input of a task_id . Returns the status of the
        requested task_id.

        :param user_ud: discogs username
        :type username: string

        :param task_id: celery job task_id
        :type task_id: string

        :return: returns a Result object
        :rtype: Result '''

    res = Result(user_id)
    res.job_id = task_id

    # skip async check if username appears invalid.
    if not is_valid_username(user_id):
        res.error = 'invalid discogs username.'
        return Response(res.render, res.mimetype)

    state = fetch_and_generate.AsyncResult(task_id)

    if state.status != 'SUCCESS' or (state.status == 'SUCCESS' and state.result == False):
        logger.error('task_id={task_id} did not return SUCCESS. result={result} and state={state}.'.format(
            task_id=task_id, result=state.result, state=state.status))
        res.error = state.status
        return Response(res.render, res.mimetype)

    res.result = state.status
    return Response(res.render, res.mimetype)


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
