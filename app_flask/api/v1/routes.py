
from couchdbkit import Server
from restkit import BasicAuth

from flask import Blueprint, g, make_response, request
from app_flask import app
from exceptions import ApiException
from . import messages_handler
from app_flask.model.message import Message

from datetime import timedelta
from flask import current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# from pprint import pprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

# Error handler for API exceptions

user_id = 'user_none'


@app.before_request
def before_request():
    """Make sure we are connected to the database for each request."""
    username = app.config.get('COUCHDB_SERVER_USERNAME')
    password = app.config.get('COUCHDB_SERVER_PASSWORD')

    if username and password:
        server = Server(app.config['COUCHDB_SERVER'],
                        filters=[BasicAuth(username, password)])
    else:
        server = Server(app.config['COUCHDB_SERVER'])

    # create databases
    g.mdb = server.get_or_create_db(app.config['COUCHDB_MESSAGES_DB'])
    Message.set_db(g.mdb)


@api.errorhandler(ApiException)
def handle_invalid_usage(error):
    response = error.to_json_response()
    app.logger.debug(error.to_dict())
    return response


# Error handler to catch endpoints that could not be found.
@app.errorhandler(404)
def not_found(error):
    error = ApiException('Endpoint not found', status_code=404)
    return error.to_json_response()



@api.route('/messages', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_messages():
    print "getting messages"
    return messages_handler.get_messages()
