import os, sys
import yaml
import argparse
from datetime import datetime

##############################
# File handling
##############################
def get_subpath(subpath:str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.abspath(os.path.join(script_dir, "../", subpath))
    try:
        os.makedirs(resolved_path)
        print(f"Created directory: {resolved_path}")
    except Exception:
        pass # Only print when directories are created
    return resolved_path

def read_file(path : str) -> str:
    """
    Reads the contents from a file.

    Gives an error if the file does not exist.
    """
    if not os.path.exists(path):
        return "" # To facilitate prepending to file

    content = ""
    try:
        f = open(path)
        content = f.read()
        f.close()
    except Exception as e:
        print(f"Error reading file from {path}")
        print(e)
        exit(1)
    return content

def write_file(path : str,
               content : str,
               mode: str = "a") -> None:
    """
    Writes the content to a file.

    If the file does not exist, it is created first.

    If the file already exists, `content` is appended to the end of the file.
    """
    try:

        os.makedirs(os.path.dirname(path),
                    exist_ok=True) # Create new directories as needed
        f = open(path, mode)
        f.write(content)
        f.close()
    except Exception as e:
        print(f"Error writing file to {path}")
        print(e)
        exit(1)
    return content

def prepend_file(path, content):
    original_content = read_file(path)
    write_file(path, content, "w")
    write_file(path, original_content, "a")

def generate_log(title, config) -> str:
    """
    Logs the current time, and `description`, to the file specified by `path`.

    If the file does not exist, it is created first.

    If the file already exists, the log is appended at the end of the file.
    """
    date, time = get_date_time()

    log = "\n---\n\n" # Separate logs, first newline needed in Markdown
    log += f"### {title}\n\n"
    log += f"> *Generated on **{date}** at **{time}**. (YYYY-MM-DD)*\n"
    
    if config["logging_enabled"]:
        log += f">\n> ```yaml\n"
        log += f"> # Config used:\n"
        log += f"> \n"
        for name, setting in config.items():
            log += f"> {name}: {setting}\n"
        log += f"> ```\n"

    return log

def get_date_time():
    """
    Returns the date and current time (`HH:MM`).
    """
    date = datetime.now().strftime("%Y-%m-%d") # Format current time
    time = datetime.now().strftime("%H:%M") # Format current time
    return [date, time]

def get_time() -> str:
    """
    Returns the current time with seconds (`HH:MM:SS`).
    """
    time = datetime.now().strftime("%H:%M:%S") # Format current time
    return time

def parse_yaml(path):
    with open(path, "r") as file:
            parsed = yaml.safe_load(file)
    return parsed

def get_config_defaults(path):
    return parse_yaml(path)

def get_skillmap(config) -> dict[str, str]:
    skillmap_path = os.path.join(config["root_dir"], config["skillmap_file"])
    return parse_yaml(skillmap_path)


##############################
# CLI arguments
##############################
def apply_cli_args(config):
    # Read defaults
    num_questions       = config["num_questions"]
    prompt_file         = config["prompt_file"]
    logging_enabled     = config["logging_enabled"]
    enumeration_enabled = config["enumeration_enabled"]
    improvement_enabled = config["improvement_enabled"]
    gpt_model           = config["gpt_model"]
    timeout             = config["timeout"]

    # Setup CLI arguments
    parser = argparse.ArgumentParser(description='Generate QBL questions using ChatGPT.')

    parser.add_argument('-n', '--num-questions',
                        type=check_num_questions_range,
                        default=num_questions,
                        help='specify how many questions per skill that ' +
                            f'should be generated (current: {num_questions})')
    parser.add_argument('-p', '--prompt-file',
                        default=prompt_file,
                        help='specify the prompt file to be used '
                            f'(current: {prompt_file})')
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='generate questions for all skills in all units')
    parser.add_argument('-u', '--units',
                        nargs='*', # Allow list of units
                        help='limit generation to a list of specified units, as named in the skillmap')
    parser.add_argument('-s', '--skills',
                        nargs='*', # Allow list of skills
                        help='limit generation to a list of specified skills, as named in the skillmap')
    parser.add_argument('-i', '--improvement-enabled',
                        type=check_boolean,
                        default=improvement_enabled,
                        choices=[True, False],
                        help='specify if an improvement step should be used, ' +
                             'set to False for saving tokens ' +
                            f'(current: {improvement_enabled})')
    parser.add_argument('-l', '--logging-enabled',
                        type=check_boolean,
                        default=logging_enabled,
                        choices=[True, False],
                        help='specify if the config should ' +
                            f'be prepended to the output file (current: {logging_enabled})')
    parser.add_argument('-e', '--enumeration-enabled',
                        type=check_boolean,
                        default=enumeration_enabled,
                        choices=[True, False],
                        help='specify if the output should be enumerated ' +
                            f'for strict ordering (current: {enumeration_enabled})')
    parser.add_argument('-gm', '--gpt-model', default=gpt_model,
                        choices=["gpt-3.5-turbo", "gpt-4"],
                        help=f'specify the GPT model to use (current: {gpt_model})')
    parser.add_argument('-t', '--timeout', type=check_timeout_range, default=timeout,
                        help=f'specify the timeout (in seconds) for requests (current: {timeout})')

    args = parser.parse_args()

    if not (args.all or args.units or args.skills):
        parser.error('you must provide at least one of the arguments: ' +
                     '-a/--all, -u/--units, or -s/--skills.')

    # Update config with args
    config["prompt_file"] = args.prompt_file
    config["num_questions"] = args.num_questions
    config["gpt_model"] = args.gpt_model
    config["timeout"] = args.timeout
    config["improvement_enabled"] = args.improvement_enabled
    config["logging_enabled"] = args.logging_enabled
    config["enumeration_enabled"] = args.enumeration_enabled
    config["all"] = args.all
    config["skills"] = args.skills
    config["units"] = args.units

    return config

def check_num_questions_range(value):
    max = 30 # More than 30 questions seems unreasonable
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"expected positive integer, was given {value}")
    if ivalue > max:
        raise argparse.ArgumentTypeError(f"maximum number of questions is {max}, was given {value}")
    return ivalue

def check_timeout_range(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"expected positive integer, was given {value}")
    return ivalue

def check_boolean(value):
    if isinstance(value, bool):
       return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"expected boolean, was given {value}")
