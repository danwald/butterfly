import importlib
import inspect
import logging
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from utils import setup_logger

logger = setup_logger("plugins")


@runtime_checkable
class Plugin(Protocol):
    def get_name(self) -> str: ...
    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool: ...
    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool: ...


class PluginManager:
    def __init__(self, plugin_dir: Path = Path("plugins"), debug: bool = False) -> None:
        self.plugin_dir = plugin_dir
        self.plugins: dict[str, Plugin] = {}
        self.debug = debug
        self.logger = setup_logger("plugins", debug)

    def discover_plugins(self) -> None:
        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                self._load_plugin(file_path)
        self.logger.info(f"Loaded {len(self.plugins)} plugins")

    def _load_plugin(self, module_file: Path) -> None:
        try:
            full_module = self.get_full_module(module_file)
            module = importlib.import_module(full_module)
            for _, klass in inspect.getmembers(module, inspect.isclass):
                if issubclass(klass, Plugin):
                    # Pass debug flag to plugin if it accepts it in __init__
                    try:
                        init_params = inspect.signature(klass.__init__).parameters
                        if "debug" in init_params:
                            plugin_inst = klass(debug=self.debug)
                        else:
                            plugin_inst = klass()
                    except ValueError:
                        # If __init__ is not inspectable, create without debug
                        plugin_inst = klass()

                    plugin_name = plugin_inst.get_name()
                    self.plugins[plugin_name] = plugin_inst
                    self.logger.info(f"Loaded plugin: {plugin_name}")
        except Exception as e:
            self.logger.error(f"Error loading plugin module {module_file}: {e}")

    def get_plugins(self) -> list[str]:
        return list(self.plugins.keys())

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

    def _run_method(
        self,
        plugin_name: str | None,
        method: str,
        *args: tuple[Any],
        **kwargs: dict[str, Any],
    ) -> bool:
        success = True
        plugins = [plugin_name] if plugin_name else self.get_plugins()
        for plugin in plugins:
            try:
                plugin_method = getattr(self.plugins[plugin], method)
                plugin_method(*args, **kwargs)
            except KeyError:
                self.logger.error(f"Plugin not found {plugin_name}")
                success = False
            except Exception as e:
                self.logger.error(f"Failed to execute {plugin_name}.{method}(): {e}")
                success = False
        return success
