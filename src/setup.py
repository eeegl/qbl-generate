import os
from util import get_skillmap, get_config_defaults, get_args, get_config

def setup():
    HOME_DIR = "../"
    CONFIG_FILE = "config.yaml"
    config_path = os.path.join(HOME_DIR, CONFIG_FILE)

    # Configure
    config_defaults = get_config_defaults(config_path)
    args = get_args(config_defaults) # For printing defaults in help
    config = get_config(config_defaults, args)
    
    print("CONFIG:") # Debug
    for c, v in config.items():
        print(c, "=", v)
    
    skillmap_path = os.path.join(config.get("root_dir"), config.get("skillmap_path"))
    skillmap = get_skillmap(skillmap_path)

    return [config, skillmap]