import importlib
import inspect
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Plugin(Protocol):
    def get_name(self) -> str: ...


class PluginManager:
    def __init__(self, plugin_dir: Path = Path("plugin")) -> None:
        self.plugin_dir = plugin_dir
        self.plugins: dict[str, Plugin] = {}

    def discover_plugins(self) -> None:
        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                self._load_plugin(file_path)
        print(f"Loaded {len(self.plugins)} plugins")

    def _load_plugin(self, module_file: Path) -> None:
        try:
            full_module = self.get_full_module(module_file)
            module = importlib.import_module(full_module)
            for _, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(klass, Plugin):
                    plugin_inst = klass()
                    plugin_name = plugin_inst.get_name()
                    self.plugins[plugin_name] = plugin_inst
                    print(f"Loaded plugin: {plugin_name}")
        except Exception as e:
            print(f"Error loading plugin module {module_file}: {e}")

    @staticmethod
    def get_full_module(module_file: Path, marker_file: str = "pyproject.toml") -> str:
        path = []
        path.append(module_file.stem)
        current = module_file.parent
        while current != current.parent:
            if (current / marker_file).exists():
                break
            path.append(current.name)
            current = current.parent

        return ".".join(reversed(path))

    def run_method(
        self, plugin_name: str, method: str, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> bool:
        try:
            plugin_method = getattr(self.plugins[plugin_name], method)
            plugin_method(*args, **kwargs)
            return True
        except KeyError:
            print(f"Plugin not found {plugin_name}")
        except Exception as e:
            print(f"Failed to execute {plugin_name}.{method}(): {e}")
        return False
