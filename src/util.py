import os
import yaml
import argparse
from datetime import datetime

def read_file(path : str) -> str:
    """
    Reads the contents from a file.

    Gives an error if the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Tried reading from {path} but file does not exist")

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

def write_log(path : str,
              description : str) -> None:
    """
    Logs the current time, and `description`, to the file specified by `path`.

    If the file does not exist, it is created first.

    If the file already exists, the log is appended at the end of the file.
    """
    try:
        f = open(path, "a")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Format current time
        f.write(f"---------- Generated {description} at {now}\n\n")
        f.close()
    except Exception as e:
        print(f"Error writing file to {path}")
        print(e)
        exit(1)

def write_file(path : str,
               content : str) -> None:
    """
    Writes the content to a file.

    If the file does not exist, it is created first.

    If the file already exists, `content` is appended to the end of the file.
    """
    try:
        f = open(path, "a")
        f.write(content + "\n\n")
        f.close()
    except Exception as e:
        print(f"Error writing file to {path}")
        print(e)
        exit(1)
    return content

def parse_yaml(path):
    with open(path, "r") as file:
            parsed = yaml.safe_load(file)
    return parsed

def get_config_defaults(path):
    return parse_yaml(path)

# args : Namespace
def get_config(config : dict[str, str], args) -> dict[str, str]:
    # config["prompts_dir"] = args.prompts_dir
    # config["responses_dir"] = args.responses_dir
    config["prompt_file"] = args.prompt_file
    config["num_questions"] = args.num_questions
    config["gpt_model"] = args.gpt_model
    config["timeout"] = args.timeout
    config["num_questions"] = args.num_questions
    return config

def get_skillmap(path : str) -> dict[str, str]:
    return parse_yaml(path)

def check_num_questions_range(value):
    max = 30
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("expected positive integer, given was %s" % value)
    if ivalue > max:
        raise argparse.ArgumentTypeError(f"maximum number of questions is {max}, given was {value}")
    return ivalue

def check_timeout_range(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("expected positive integer, given was %s" % value)

def get_args(config):
    num_questions = config.get("num_questions")
    prompt_file = config.get("prompt_file")
    improvement_enabled = config.get("improvement_enabled")
    gpt_model = config.get("gpt_model")
    request_timeout = config.get("request_timeout")

    parser = argparse.ArgumentParser(description='Generate QBL questions using AI.')

    parser.add_argument('-n', '--num-questions', type=check_num_questions_range, default=num_questions,
                        help=f'specify how many questions per skill that should be generated (default: {num_questions})')
    parser.add_argument('-p', '--prompt-file', default=prompt_file,
                        help=f'specify the prompt file to be used (default: {prompt_file})')
    parser.add_argument('-u', '--unit',
                        help='limit generation to the specified unit')
    parser.add_argument('-s', '--skill',
                        help='limit generation to the specified skill')
    parser.add_argument('-i', '--improvement-enabled', default=improvement_enabled,
                        choices=[True, False],
                        help=f'specify if an improvement step should be used, set to False for saving tokens (default: {improvement_enabled})')
    parser.add_argument('-gm', '--gpt-model', default=gpt_model,
                        choices=["gpt-3.5-turbo", "gpt-4"],
                        help=f'specify the GPT model to use (default: {gpt_model})')
    parser.add_argument('-t', '--timeout', type=check_timeout_range, default=request_timeout,
                        help=f'specify the timeout (in seconds) for requests (default: {request_timeout})')

    return parser.parse_args()
