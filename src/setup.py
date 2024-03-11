import os
from util import get_config, get_skillmap, get_args

def setup():
    CONFIG_DIR = "../"
    CONFIG_FILE = "config.yaml"

    config = get_config(os.path.join(CONFIG_DIR, CONFIG_FILE))
    args = get_args(config)

    return { config, args }