from typing import TypedDict


class Request(TypedDict):
    pass
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
    pass
# end def


def get_requests() -> list[Request]:
    return []
# end def
