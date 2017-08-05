import logging
import requests
from flask import Flask, request, abort
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

GITHUB_BASE_URL = "https://api.github.com"


@app.route('/github/repositories/')
def github_repositories():
    username = request.args.get('username', None)
    if username is None:
        abort(400, "username is a required query param.")

    # https://developer.github.com/v3/repos/#list-user-repositories
    response = requests.get("{}/users/{}/repos".format(GITHUB_BASE_URL, username))

    if response.status_code == 404:
        abort(404, "username {} not found".format(username))
    elif response.status_code != 200:
        logging.error("Request to github failed. Code {}. Error: {}".format(
            response.status_code, response.content))
        abort(500, "request to github failed")

    repositories = response.json()

    order_by = request.args.get('order_by', None)
    if order_by:
        if order_by[0] == '-':
            reverse = True
            order_by = order_by[1:]
        else:
            reverse = False
        try:
            repositories = sorted(repositories, key=lambda a: a[order_by], reverse=reverse)
        except KeyError:
            abort(400, "Invalid order_by, {}".format(order_by))

    limit = request.args.get('limit', None)
    if limit is not None:
        try:
            limit = int(limit)
        except:
            abort(400, "limit must be an integer, got {}".format(limit))
        repositories = repositories[:limit]
    return json.dumps(repositories)


@app.route('/')
def hello():
    return json.dumps({'hello': 'world'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
