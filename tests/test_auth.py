import time
from pathlib import Path
from typing import Generator, Self

import pytest

from interfaces.auth import BearerAuth, BlueSkyAuth, HashableMixin, SessionCacheMixin


class GrantedAuth:
    def authorize(self: Self) -> bool:
        return True


@pytest.fixture
def auth() -> GrantedAuth:
    return GrantedAuth()


def test_auth(auth: GrantedAuth) -> None:
    assert auth.authorize()


class FSCache(HashableMixin, SessionCacheMixin):
    pass


@pytest.fixture(scope="function")
def fake_session_cache() -> Generator[FSCache, None, None]:
    fname = ".test-session"
    secs = 200.0

    yield FSCache()._override_defaults(fname, secs)

    Path(fname).unlink(missing_ok=True)  # might delete because stale


@pytest.mark.parametrize(
    "access_token,is_valid,header_output",
    (
        ("", False, {"Authorization": "Bearer "}),
        (None, False, {"Authorization": "Bearer None"}),
        ("foobar", True, {"Authorization": "Bearer foobar"}),
    ),
)
def test_bearer_auth(
    access_token: str, is_valid: bool, header_output: dict[str, str]
) -> None:
    bt = BearerAuth(access_token=access_token)
    assert bool(bt) == is_valid
    if not bt:
        with pytest.raises(ValueError):
            assert bt.header == header_output
    else:
        assert bt.header == header_output


def test_session_cache_retervial(fake_session_cache: FSCache) -> None:
    assert not fake_session_cache.get_session()
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"
    fake_session_cache.save_session("barfoo")
    assert fake_session_cache.get_session() != "foobar"
    assert fake_session_cache.get_session() == "barfoo"


def test_session_cache_file(fake_session_cache: FSCache) -> None:
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"


def test_session_cache_stale_file(fake_session_cache: FSCache) -> None:
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"

    fake_session_cache._update_session_time(
        time.time() - fake_session_cache.stale_seconds
    )
    assert not fake_session_cache.get_session()


def test_bluesky_hashable() -> None:
    ba = BlueSkyAuth("foo", "bar")
    assert hash(ba)

    ba.save_session("hello")
    assert ba.get_session() == "hello"
    Path(ba.session_filename).unlink(missing_ok=True)
