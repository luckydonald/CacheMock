from html import escape

from flask import Flask, url_for, request, redirect

import storage
app = Flask(__name__)

HIDDEN_PATH = '__proxy__'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not storage.is_setup():
        url = url_for(settings_index.__name__)
        return f"""YOU NEED TO SETUP FIRST\n\n<br><a href="{url}">Click here</a> or<br>\n\ngo to: {url}"""
    # end if
    return 'You want path: %s' % path
# end def



@app.route(f'/{HIDDEN_PATH}/')
def settings_index():
    if not storage.is_setup():
        url = url_for(proxy_setup.__name__)
        # redirect to proxy_setup
        return redirect(url, code=302)  # temp redirect
    return f"""
    <ul>
    <li><a href="{escape(url_for(proxy_setup.__name__))}">Proxy URL settings</a></li>
    </ul>
    """
# end def


@app.route(f'/{HIDDEN_PATH}/setup/proxy', methods=['GET', 'POST'])
def proxy_setup():
    if request.method != "POST":
        # return a form with a single input field for setting the proxy
        proxy = storage.get_setup_proxy()
        proxy = escape(proxy) if proxy else "https://example.com:443/path/"
        return f"""
            <h1>Proxy URL settings</h1>
            <style>
                input {'{'}
                    width: 100%;
                    padding: 0.5em;
                    margin: 0.5em;
                {'}'}
            </style>
            <form method="POST">
                <input name="proxy" value="{proxy}"/><br>
                <input type="submit" value="Submit">
            </form>
        """
    else:
        # get the "proxy" POST variable, store it
        proxy = request.form.get("proxy")
        storage.set_setup_proxy(proxy)
        return f"""
            <h1>Proxy URL settings</h1>
            <h2>✅ Proxy settings saved</h2>
            <a href="{url_for(settings_index.__name__)}">back</a>
        """
    # end if
# end def




if __name__ == '__main__':
    app.run()
