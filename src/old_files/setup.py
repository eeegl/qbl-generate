import os
from util import get_skillmap, get_config_defaults, apply_cli_args

def setup():
    HOME_DIR = "../"
    CONFIG_FILE = "config.yaml"
    config_path = os.path.join(HOME_DIR, CONFIG_FILE)

    config_defaults = get_config_defaults(config_path)
    config = apply_cli_args(config_defaults)
    skillmap = get_skillmap(config)

    print_config(config) # For debugging

    return [config, skillmap]

def print_config(config):
    print("--- Config used:")
    # Determine the maximum key length
    max_key_length = max(len(key) for key in config.keys())
    # Use this length to align the keys to the right
    for c, v in config.items():
        print(f"{c:>{max_key_length}} = {v}")
    print()