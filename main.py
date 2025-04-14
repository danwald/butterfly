import argparse
from pathlib import Path

from plugins import PluginManager


def main() -> None:
    parser = argparse.ArgumentParser(description="Butterfly application")
    parser.add_argument(
        "--plugin-dir", type=Path, help="Directory to search for plugins"
    )
    parser.add_argument(
        "--list-plugins", action="store_true", help="List available plugins and exit"
    )
    parser.add_argument("--plugin", help="Specify plugin to use")
    parser.add_argument("--method", help="Method to execute on the plugin")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.plugin_dir:
        pm = PluginManager(plugin_dir=args.plugin_dir)
    else:
        pm = PluginManager()

    pm.discover_plugins()

    if args.list_plugins:
        print("Available plugins:")
        for plugin_name in pm.plugins:
            print(f"  - {plugin_name}")
        return

    if args.plugin and args.method:
        success = pm.run_method(args.plugin, args.method)
        if not success:
            exit(1)


if __name__ == "__main__":
    main()
