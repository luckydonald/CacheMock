from flask import Blueprint, url_for

import storage
from routes.ui import ui, settings_index

wildcard = Blueprint('wildcard', __name__)



@wildcard.route('/', defaults={'path': ''})
@wildcard.route('/<path:path>', )
def catch_all(path):
    if not storage.is_setup():
        url = url_for(f"{ui.name}.{settings_index.__name__}")
        return f"""YOU NEED TO SETUP FIRST\n\n<br><a href="{url}">Click here</a> or<br>\n\ngo to: {url}"""
    # end if
# end def
