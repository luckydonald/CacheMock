import json
from html import escape
from urllib.parse import urlencode

from flask import Blueprint, request, url_for, redirect, Response as FlaskResponse

import storage
from utils import is_json_content_type

ui = Blueprint('ui', __name__)



@ui.route(f'/')
def settings_index():
    if not storage.is_setup():
        url = url_for(f"{ui.name}.{proxy_setup.__name__}")
        # redirect to proxy_setup
        return redirect(url, code=302)  # temp redirect
    return f"""
    <ul>
    <li><a href="{escape(url_for(f"{ui.name}.{proxy_setup.__name__}"))}">Proxy URL settings</a></li>
    <li><a href="{escape(url_for(f"{ui.name}.{proxy_requests.__name__}"))}">Stored Routes</a></li>
    </ul>
    """
# end def


@ui.route(f'/setup/proxy', methods=['GET', 'POST'])
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
            <a href="{url_for(f"{ui.name}.{settings_index.__name__}")}">back</a>
        """
    # end if
# end def

@ui.route(f'/requests')
def proxy_requests():
    requests = storage.get_requests()
    return f"""
    <ul>
    {"\n".join([
        f"""
        <li>
            <a href="{url_for(f"{ui.name}.{proxy_request.__name__}", request_pk=index)}">
            {escape(req.name).join(["<h4>", "</h4>"]) if req.name else ''}
            {req.html()}
            </a>
        </li>
        """
        for index, req in enumerate(requests)
    ])}
    </ul>
    """
# end def

@ui.route('/requests/<int:request_pk>')
def proxy_request(request_pk: int):
    req = storage.get_request(request_pk)
    if request.headers['Accept'] == 'application/json':
        if req is None:
            return FlaskResponse(
                response=f"""{
                    "ok": false,
                    "status": 404,
                    "reason": "Not Found",
                    "message": "The caching entry with id {request_pk} does not exist."
                }""",
                status=404,
                mimetype="application/json",
            )
        # end if
        return FlaskResponse(
            response=req.dump_json(),
            status=200,
            mimetype='application/json',
            content_type='application/json',
        )
    else:
        if req is None:
            return FlaskResponse(
                response=f"""
                <h1>Not Found</h1>
                <hr />
                The caching entry with id <code>{request_pk}</code> does not exist.
                """,
                status=404,
                mimetype="text/html",
            )
        # end if
        return FlaskResponse(
            response=f"""
                {req.html()}<br>
                {f'<h3>Request Body</h3><pre>{req.request.data}</pre>' if is_json_content_type(req.request.headers.get('Content-Type')) else ''}
                {f'<h3>Response Body</h3><pre>{req.response.content}</pre>' if is_json_content_type(req.response.headers.get('Content-Type')) else ''}
                <h3>Full dump:</h3>
                <pre>{req.dump_json()}</pre>
            """,
            status=200,
        )
    # end if
# end def
