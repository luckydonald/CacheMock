from html import escape
from typing import Any

from flask import Blueprint, url_for, request as flask_request, Response as FlaskResponse
import requests
from flask_cors import cross_origin

import storage
from routes.ui import ui, settings_index
from storage import Response, Request

wildcard = Blueprint('wildcard', __name__)

# NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
EXCLUDED_HEADERS = [
    'content-encoding',
    'content-length',
    'transfer-encoding',
    'connection',
]


ALL_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@cross_origin()
@wildcard.route('/', defaults={'path': ''}, methods=ALL_METHODS)
@wildcard.route('/<path:path>', methods=ALL_METHODS)
def catch_all(path: str):
    if not storage.is_setup():
        url = url_for(f"{ui.name}.{settings_index.__name__}")
        return f"""YOU NEED TO SETUP FIRST\n\n<br><a href="{url}">Click here</a> or<br>\n\ngo to: {url}"""
    # end if

    # noinspection PyArgumentList
    request = Request(
        method=flask_request.method,
        url=f"{storage.get_setup_proxy()}{path}",
        query=flask_request.args,
        headers={k: v for k, v in flask_request.headers if k.lower() != 'host'},  # exclude 'host' header
        data=flask_request.get_data(),
        cookies=flask_request.cookies,
    )

    match = storage.match_request(request)
    pk = None

    if match:
        pk, req = match
        if req.is_cached():
            return FlaskResponse(
                response=req.response.content,
                headers=req.response.headers,
                status=req.response.status_code,
            )
        # end if
    # end if

    try:
        flask_response = requests.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            params=request.query,
            data=request.data,
            cookies=request.cookies,
            allow_redirects=False,  # we want to have the client reproduce that ourselves
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        return FlaskResponse(
            response=f"""
                <h1>Bad Gateway</h1>
                <hr />
                Could not connect to the gateway at <a href="{escape(request.url)}">{escape(request.url)}</a>.
            """,
            status=502,
        )
    except requests.exceptions.Timeout:
        return FlaskResponse(
            response=f"""
                <h1>Gateway Timeout</h1>
                <hr />
                Could not connect to the gateway at <a href="{escape(request.url)}">{escape(request.url)}</a>.
            """,
            status=504,
        )
    # end try

    # exclude some keys in response that would interfere with what we send ourselves
    headers = {
        k: v for k, v in flask_response.raw.headers.items()
        if k.lower() not in EXCLUDED_HEADERS
    }

    # noinspection PyArgumentList
    response: Any = Response(
        content=flask_response.content,
        status_code=flask_response.status_code,
        headers=headers,
    )
    response: Response

    storage.set_cache(
        pk=pk,
        request=request,
        response=response,
    )

    flask_response = FlaskResponse(
        response=response.content,
        status=response.status_code,
        headers=headers,
    )
    return flask_response
# end def
