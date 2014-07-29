from werkzeug.contrib.fixers import ProxyFix
from app_flask import app

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT'])
