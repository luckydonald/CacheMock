from flask import Flask, url_for

import storage
from routes.ui import ui, settings_index
from secrets import HIDDEN_PATH

app = Flask(__name__)

app.register_blueprint(ui.ui, url_prefix=HIDDEN_PATH)




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not storage.is_setup():
        url = url_for(f"{ui.name},{settings_index.__name__}")
        return f"""YOU NEED TO SETUP FIRST\n\n<br><a href="{url}">Click here</a> or<br>\n\ngo to: {url}"""
    # end if
    return 'You want path: %s' % path
# end def



if __name__ == '__main__':
    app.run()
