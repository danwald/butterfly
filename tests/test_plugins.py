import sys
from pathlib import Path

import pytest

from plugins import PluginManager


@pytest.fixture
def manager() -> PluginManager:
    current_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(current_dir))
    return PluginManager(plugin_dir=current_dir / "plugins").discover_plugins()


def test_plugin_manager(manager: PluginManager) -> None:
    assert manager._run_method("hello", "execute", ("arg1",), key="value")
    assert manager._run_method("hello", "validate", ("arg1",), key="value")
    assert manager._run_method("hello", "doesnt_exist") is False
    assert manager._run_method("doesnt_exist", "404") is False


def test_supported_plugins() -> None:
    supported_plugins = PluginManager().discover_plugins()
    for plugin in supported_plugins.get_plugins():
        assert supported_plugins._run_method(plugin, "get_name")
