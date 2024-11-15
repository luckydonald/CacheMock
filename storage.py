from typing import TypedDict
from pydantic.dataclasses import dataclass

@dataclass
class Response:
    content: bytes
    status_code: int
    headers: dict[str, str]
# end class


@dataclass
class Request:
    name: str | None
    path: str
    response: Response | None
# end class


class Data(TypedDict):
    proxy: None | str
    requests: list[Request]
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

def add_request(request: Request) -> None:
    data["requests"].append(request)
# end def


def get_requests() -> list[Request]:
    return data["requests"][:]
# end def


def get_request(pk: int) -> Request:
    return data["requests"][pk]
# end def

def match_request(path: str) -> Request | None:
    return None
# end def

def set_cache(
    *,
    pk: int,
    name: str | None,
    path: str,
    response: Response | None,
) -> None:
    return None
# end def