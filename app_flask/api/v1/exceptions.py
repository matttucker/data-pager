from flask import jsonify, Response

ApiErrors = {}
# misc errors
ApiErrors[00000] = {'description': "Standard error."}


#
# Error Handling
#
class ApiException(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None,
                 code=None, payload=None, suppress_response_codes=False):
        Exception.__init__(self)

        self.code = code
        if code and not message:
            self.message = ApiErrors[code]['description']
        else:
            self.message = message

        if status_code:
            self.status_code = status_code
        self.payload = payload
        self.suppress_response_codes = suppress_response_codes

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status'] = self.status_code
        if self.code:
            rv['code'] = self.code
        rv['error'] = self.message
        return rv

    def to_json_response(self):
        response = jsonify(self.to_dict())
        if self.suppress_response_codes:
            response.status_code = 200
        else:
            response.status_code = self.status_code

        if self.status_code == 401:
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials : ' +
                self.message, 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})

        return response


def raise_field_required_exception(field):
    raise ApiException(
        "Field '{field}' is required.".format(field=field), status_code=400)
