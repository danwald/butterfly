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
    parser.add_argument(
        "--plugins",
        nargs="*",
        help="Specify plugin to use (all)",
    )
    parser.add_argument(
        "--method",
        help="Method to execute on the plugin",
        choices=["validate", "execute"],
    )
    parser.add_argument("--message", type=str, help="text content to post")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.plugin_dir:
        pm = PluginManager(plugin_dir=args.plugin_dir)
    else:
        pm = PluginManager()

    pm.discover_plugins()

    if not args.method or args.list_plugins:
        print("Available plugins:")
        for plugin_name in pm.plugins:
            print(f"  - {plugin_name}")
        return

    for plugin in args.plugins or [""]:
        if args.method == "execute" and not args.message:
            print("You need to provide content to post")
            break
        pm._run_method(plugin, args.method, args.message)


if __name__ == "__main__":
    main()
