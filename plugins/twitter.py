from typing import Any


class Twitter:
    def __init__(self) -> None:
        self.name = "twitter"

    def get_name(self) -> str:
        return self.name

    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        print(f"{self.name} plugin's execute() called with {args},{kwargs}")
        return True

    def validate(self) -> bool:
        print(f"{self.name} plugin's validate()")
        return True
