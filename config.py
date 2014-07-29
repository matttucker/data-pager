
print "Booting default config."
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

PRIVATE_URL_BASE = "http://{host}:{port}".format(host=HOST, port=PORT)
PUBLIC_URL_BASE = PRIVATE_URL_BASE
TEMP_FILE_FOLDER = "../tmp"

COUCHDB_SERVER = "http://localhost:5984"
COUCHDB_MESSAGES_DB= "messages"

SECRET_KEY = "secret"
