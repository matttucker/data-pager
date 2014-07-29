#!/usr/bin/env python
from datetime import datetime


def now_string():
    return datetime.utcnow().isoformat()


def parse_boolean(str):
    return str.lower() in ("yes", "true", "t", "1")


def get_limit_from_query_params(params, default=25):
    if "limit" in params:
        try:
            limit = int(params['limit'])
        except ValueError:
            raise ApiException(
                "Parameter 'limit={value}' could not parsed.".format(
                    value=params['limit']),
                status_code=400)

        if limit <= 0:
            raise ApiException(
                "Parameter 'limit={value}' must be greater than 0.".format(
                    value=params['limit']),
                status_code=400)
    else:
        limit = default

    return limit


def get_skip_from_query_params(params):
    print(params)
    if 'skip' in params:
        try:
            skip = int(params['skip'])
        except ValueError:
            raise ApiException(
                "Parameter 'skip={value}' could not parsed.".format(
                    value=params['skip']),
                status_code=400)

        if skip < 0:
            raise ApiException(
                "Parameter 'skip={value}' must be greater than or equal to 0.".format(
                    value=params['skip']),
                status_code=400)
    else:
        print("no skip")
        skip = None

    print "skip:", skip
    return skip


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
