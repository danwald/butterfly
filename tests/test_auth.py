import pytest


class GrantedAuth:
    def authorize(self) -> bool:
        return True


@pytest.fixture
def auth():
    return GrantedAuth()


def test_auth(auth):
    assert auth.authorize()
