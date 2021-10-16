import os
import sys
import argparse

# TODO Control which of these:
#       https://github.com/username/projectname.git
#  vs
#           git@github.com:username/projectname.git

from utils import (
    get_json_from_github
)
from utils import PLUGINS_JSON_FILE, THEMES_JSON_FILE
from dirutils import use_directory


# From https://stackoverflow.com/q/11415570/104370
def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def clone_repo(plugin):
    repo = plugin.get("repo")
    branch = plugin.get("branch", "master")
    user = repo.split("/")[0]
    with use_directory(user, create_if_missing=True):
        print(f"git clone https://github.com/{repo}.git")


def process_released_plugins(overwrite=False):
    with use_directory("plugins", create_if_missing=True):
        plugin_list = get_json_from_github(PLUGINS_JSON_FILE)
        for plugin in plugin_list:
            clone_repo(plugin)


def process_released_themes(overwrite=False):
    print("-----\nProcessing themes....\n")
    with use_directory("css-themes", create_if_missing=True):
        theme_list = get_json_from_github(THEMES_JSON_FILE)
        for theme in theme_list:
            clone_repo(theme)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Create notes based on the obsidian-releases repo"
    )
    parser.add_argument('-o', '--output_directory', type=readable_dir, default='.')
    args = parser.parse_args(argv)

    with use_directory(args.output_directory, create_if_missing=False):
        print(f"Working directory: {os.getcwd()}")
        process_released_plugins(args.overwrite)
        process_released_themes(args.overwrite)


if __name__ == "__main__":
    main()
