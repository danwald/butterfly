from plugins import PluginManager


def main() -> None:
    pm = PluginManager()
    pm.discover_plugins()


if __name__ == "__main__":
    main()
