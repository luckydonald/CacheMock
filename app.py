from flask import Flask

from flask_cors import CORS

from routes.ui import ui
from routes.wildcard import wildcard
from env_secrets import HIDDEN_PATH

app = Flask(__name__)
CORS(app)

app.register_blueprint(wildcard, url_prefix="")
app.register_blueprint(ui, url_prefix=HIDDEN_PATH)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
