from interfaces.social import Content


class SocialTestContent(Content):
    def __init__(self, data: str) -> None:
        self.data = data


class SocialTester:
    def post(self, cnt: Content) -> bool:
        return True

    def validate(self) -> bool:
        return True


def test_social():
    assert SocialTester().post(SocialTestContent("foobar"))
    assert SocialTester().validate()
