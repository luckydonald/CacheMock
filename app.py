from flask import Flask, url_for
import requests

import storage
from routes.ui import ui
from routes.wildcard import wildcard
from env_secrets import HIDDEN_PATH

app = Flask(__name__)

app.register_blueprint(wildcard, url_prefix="")
app.register_blueprint(ui, url_prefix=HIDDEN_PATH)


if __name__ == '__main__':
    app.run()
