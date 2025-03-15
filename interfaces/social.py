from typing import Protocol


class Content: ...


class Social(Protocol):
    def post(self, content: Content) -> bool: ...
