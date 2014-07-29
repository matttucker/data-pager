from flask import Flask
import logging

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SERVER_CONFIG', silent=True)


#  Logging
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
app.logger.handlers[0].setFormatter(formatter)
app.logger.info("Initializing server...")

from app_flask.api.v1.routes import api
app.register_blueprint(api)

# from site import site
# app.register_blueprint(site)

# Disable static file caching for development only so that changes to
# CSS and Javascript are seen immediately by the browser.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

app.secret_key = app.config['SECRET_KEY']

