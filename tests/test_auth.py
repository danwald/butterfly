import os
from pathlib import Path

import pytest

from interfaces.auth import BearerAuth, BlueSkyAuth, HashableMixin, SessionCacheMixin


class GrantedAuth:
    def authorize(self) -> bool:
        return True


@pytest.fixture
def auth():
    return GrantedAuth()


def test_auth(auth):
    assert auth.authorize()


@pytest.fixture(scope="function")
def fake_session_cache():
    fname = ".test-bs-session"
    secs = 200

    class FSCache(HashableMixin, SessionCacheMixin):
        pass

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
def test_bearer_auth(access_token, is_valid, header_output):
    bt = BearerAuth(access_token=access_token)
    assert bool(bt) == is_valid
    if not bt:
        with pytest.raises(ValueError):
            assert bt.header == header_output
    else:
        assert bt.header == header_output


def test_session_cache_retervial(fake_session_cache):
    assert not fake_session_cache.get_session()
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"
    fake_session_cache.save_session("barfoo")
    assert fake_session_cache.get_session() != "foobar"
    assert fake_session_cache.get_session() == "barfoo"


def update_file_mod_time(path: Path, secs: int) -> None:
    mod_time = path.stat().st_mtime
    os.utime(path, (mod_time + secs, mod_time + secs))


def test_session_cache_file(fake_session_cache):
    session_path = Path(fake_session_cache.session_filename)
    assert not session_path.exists()
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"
    assert session_path.exists()


def test_session_cache_stale_file(fake_session_cache):
    session_path = Path(fake_session_cache.session_filename)
    fake_session_cache.save_session("foobar")
    assert fake_session_cache.get_session() == "foobar"
    assert session_path.exists()

    update_file_mod_time(session_path, fake_session_cache.stale_seconds)
    assert fake_session_cache.get_session() == "foobar"
    assert session_path.exists()

    update_file_mod_time(session_path, -1 * fake_session_cache.stale_seconds)
    assert not fake_session_cache.get_session()
    assert not session_path.exists()


def test_bluesky_hashable():
    ba = BlueSkyAuth("foo", "bar")
    assert hash(ba)
