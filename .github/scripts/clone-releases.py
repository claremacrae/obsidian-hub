import sys
import argparse

# TODO Control which of these:
#       https://github.com/username/projectname.git
#  vs
#           git@github.com:username/projectname.git

from utils import (
    get_json_from_github
)
from utils import PLUGINS_JSON_FILE, THEMES_JSON_FILE, OUTPUT_DIR


def clone_repo(plugin):
    repo = plugin.get("repo")
    branch = plugin.get("branch", "master")
    user = repo.split("/")[0]
    print(f"git clone https://github.com/{repo}.git")


def process_released_plugins(overwrite=False):
    plugin_list = get_json_from_github(PLUGINS_JSON_FILE)
    for plugin in plugin_list:
        clone_repo(plugin)


def process_released_themes(overwrite=False):
    print("-----\nProcessing themes....\n")
    theme_list = get_json_from_github(THEMES_JSON_FILE)
    for theme in theme_list:
        clone_repo(theme)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Create notes based on the obsidian-releases repo"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing files."
    )
    args = parser.parse_args(argv)

    process_released_plugins(args.overwrite)
    process_released_themes(args.overwrite)


if __name__ == "__main__":
    main()
