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
        "--execute",
        action="store_true",
        help="Execute the plugin (default is validate)",
    )
    parser.add_argument("--message", type=str, help="text content to post")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    pm = PluginManager(plugin_dir=args.plugin_dir or None).discover_plugins()

    if args.list_plugins:
        print("Available plugins:")
        for plugin_name in pm.plugins:
            print(f"  - {plugin_name}")
        return

    # Default to "validate", use "execute" if --execute flag is set
    method = "execute" if args.execute else "validate"

    for plugin in args.plugins or [""]:
        if method == "execute" and not args.message:
            print("You need to provide content to post")
            break
        pm._run_method(plugin, method, args.message)


if __name__ == "__main__":
    main()
