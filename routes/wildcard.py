from flask import Blueprint, url_for, request as flask_request, Response as FlaskResponse
import requests

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


@wildcard.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'HEAD'])
@wildcard.route('/<path:path>', methods=['GET', 'POST', 'HEAD'])
def catch_all(path: str):
    if not storage.is_setup():
        url = url_for(f"{ui.name}.{settings_index.__name__}")
        return f"""YOU NEED TO SETUP FIRST\n\n<br><a href="{url}">Click here</a> or<br>\n\ngo to: {url}"""
    # end if

    # noinspection PyArgumentList
    request = Request(
        method=flask_request.method,
        url=f"{storage.get_setup_proxy()}{path}",
        headers={k: v for k, v in flask_request.headers if k.lower() != 'host'},  # exclude 'host' header
        data=flask_request.get_data(),
        cookies=flask_request.cookies,
    )

    match = storage.match_request(request)
    pk = None

    if match:
        pk, req = match
        if req.response is not None:
            return FlaskResponse(
                response=req.response.content,
                headers=req.response.headers,
                status=req.response.status_code,
            )
        # end if
    # end if

    response = requests.request(
        method=request.method,
        url=request.url,
        headers=request.headers,
        data=request.data,
        cookies=request.cookies,
        allow_redirects=False,  # we want to have the client reproduce that ourselves
    )

    # exclude some keys in response that would interfere with what we send ourselves
    headers = [
        (k, v) for k, v in response.raw.headers.items()
        if k.lower() not in EXCLUDED_HEADERS
    ]
    # endregion exclude some keys in :res response

    storage.set_cache(
        pk=pk,
        request=request,
        response=Response(),
    )

    flask_response = FlaskResponse(response.content, response.status_code, headers)
    return flask_response
# end def
