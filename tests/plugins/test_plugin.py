class HelloPlugin:
    def __init__(self):
        self.name = "hello"

    def get_name(self):
        return self.name

    def execute(self, *args, **kwargs):
        print(f"{self.name} plugin's execute() called with {args},{kwargs}")
        return True

    def validate(self, *args, **kwargs):
        print(f"{self.name} plugin's validate() called with {args},{kwargs}")
        return True
