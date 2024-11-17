from html import escape
from typing import TypedDict, Self, Any
from urllib.parse import urlencode

from pydantic import RootModel
from pydantic.dataclasses import dataclass

@dataclass
class Response:
    content: bytes
    status_code: int
    headers: dict[str, str | list[str]]
# end class


@dataclass
class Request:
    method: str
    url: str
    query: dict[str, str | list[str]]
    headers: dict[str, str | list[str]]
    data: str
    cookies: dict[str, str]

    def match(self, request: Self) -> bool:
        return (
            self.method == request.method
            and self.url == request.url
            and self.query == request.query
            and self.headers == request.headers
            and self.data == request.data
            and self.cookies == request.cookies
        )
    # end def
# end class


@dataclass
class Cache:
    name: str | None
    # path: str
    request: Request
    response: Response | None

    def is_cached(self) -> bool:
        return (
            self.response is not None
            and self.response.status_code not in range(500, 600)
        )
    # end if

    def update(self, request: Self) -> Self:
        self.name = request.name
        # self.path = request.path
        self.response = request.response
        return self
    # end def

    def match(self, request: Self) -> bool:
        return self.request.match(request.request)
    # end def

    def dump_json(self):
        return RootModel[self.__class__](self).model_dump_json(indent=4)

    def html(self):
        return f"""
        <code>{escape(self.request.method)}</code>
        {escape(self.request.url)}{'?' if self.request.query else ''}{escape(urlencode(self.request.query, doseq=True))}
        """
# end class


class Data(TypedDict):
    proxy: None | str
    requests: list[Cache]
# end class


data: Data = {
    "proxy": None,
    "requests": [],
}


def is_setup() -> bool:
    return (
        data["proxy"] is not None
    )
# end def

def get_setup_proxy() -> str | None:
    return data["proxy"]
# end def


def set_setup_proxy(proxy: str) -> None:
    data["proxy"] = proxy
# end def


def add_request(request: Cache) -> None:
    data["requests"].append(request)
# end def


def get_requests() -> list[Cache]:
    return data["requests"][:]
# end def


def get_request(pk: int) -> Cache | None:
    try:
        return data["requests"][pk]
    except IndexError:
        return None
# end def

def match_request(search: Request) -> tuple[int, Cache] | None:
    reqs = [
        (index, req)
        for index, req
        in enumerate(data["requests"])
        if req.request.match(search)
    ]
    if len(reqs) == 0:
        return None
    elif len(reqs) == 1:
        return reqs[0]
    else:
        raise KeyError(f'No matching request: {search.method} {search.url}')
# end def

def set_cache(
    *,
    pk: int,
    request: Request,
    response: Response | None,
) -> None:
    request: Any = Cache(
        name=None,
        request=request,
        response=response,
    )
    request: Cache
    if pk in data["requests"]:
        data["requests"][pk].update(request)
    else:
        add_request(request)
    # end if
# end def