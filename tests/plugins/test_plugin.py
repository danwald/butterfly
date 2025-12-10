from typing import Any


class HelloPlugin:
    def __init__(self) -> None:
        self.name = "hello"

    def get_name(self) -> str:
        return self.name

    def execute(self, *args: Any, **kwargs: Any) -> bool:
        print(f"{self.name} plugin's execute() called with {args},{kwargs}")
        return True

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        print(f"{self.name} plugin's validate() called with {args},{kwargs}")
        return True
