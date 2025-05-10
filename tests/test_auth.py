import pytest

from interfaces.auth import BearerAuth


class GrantedAuth:
    def authorize(self) -> bool:
        return True


@pytest.fixture
def auth():
    return GrantedAuth()


def test_auth(auth):
    assert auth.authorize()


@pytest.mark.parametrize(
    "access_token,is_valid,header_output",
    (
        ("", False, {"Authorization": "Bearer "}),
        (None, False, {"Authorization": "Bearer None"}),
        ("foobar", True, {"Authorization": "Bearer foobar"}),
    ),
)
def test_bearer_auth(access_token, is_valid, header_output):
    bt = BearerAuth(access_token=access_token)
    assert bool(bt) == is_valid
    if not bt:
        with pytest.raises(ValueError):
            assert bt.header == header_output
    else:
        assert bt.header == header_output
