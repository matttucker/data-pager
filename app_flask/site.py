from flask import Blueprint, current_app, send_file, render_template_string
from werkzeug.exceptions import NotFound
import os
from app_flask import app
from pprint import pprint

site = Blueprint('site', __name__)


@site.route('/', defaults={'path': 'index.html'})
@site.route('/<path:path>')
def serve_index(path):
    print "path: ", path
    # flask_yeoman_debug = int(os.environ.get('FLASK_YEOMAN_DEBUG', False))

    # While developing, we serve the app directory
    # if flask_yeoman_debug:
    if app.config['DEBUG']:
        fpath = 'app'
    else:
        fpath = 'dist'

    root_path = os.path.dirname(current_app.root_path)
    default_path = os.path.join(root_path, fpath)
    print "default path: ", default_path

    default_path_abs = os.path.join(default_path, path)

    if os.path.isfile(default_path_abs):
        # if path == 'index.html' or path == 'api.html':
        #     # If index.html is requested, we inject the Flask current_app
        #     # config
        #     return render_template_string(
        #         open(default_path_abs).read().decode('utf-8'),
        #         config=current_app.config)
        return send_file(default_path_abs)

    # While development, we must check the .tmp dir as fallback
    if app.config['DEBUG']:
        # The .tmp dir is used by compass and for the template file
        alt_path = os.path.join(root_path, '.tmp')
        alt_path_abs = os.path.join(alt_path, path)
        if os.path.isfile(alt_path_abs):
            return send_file(alt_path_abs)

    raise NotFound()
