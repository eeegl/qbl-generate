import os, re
import yaml
from datetime import datetime

def read_file(path:str) -> str:
    """Reads the contents from a file.

    Gives an error if the file does not exist."""
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

def write_file(path:str, content:str, mode:str = "a") -> None:
    """ Writes the content to a file.

    If the file does not exist, it is created first.

    If the file already exists, `content` is appended to the end of the file. """
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

# FIXME: remove this
# def prepend_file(path, content):
#     original_content = read_file(path)
#     write_file(path, content, "w")
#     write_file(path, original_content, "a")

def parse_yaml(path):
    with open(path, "r") as file:
            parsed = yaml.safe_load(file)
    return parsed

def get_openai_key(key_name = "OPENAI_API_KEY_KTH") -> str:
    """Helper function that gets the OpenAI API key saved  an environmental variable,
    by default set to `OPENAI_API_KEY_KTH`.

    NOTE: Make sure that `OPENAI_API_KEY_KTH` is set, or provide an argument
    if you have it set to another variable name."""
    key = os.getenv(key_name) 
    if not key:
        raise ValueError(f"Environment variable {key_name} is not set.")
    return key

def get_subpath(subpath:str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.abspath(os.path.join(script_dir, "../", subpath))
    try:
        os.makedirs(resolved_path)
        print(f"Created directory: {resolved_path}")
    except Exception:
        pass # Only print when directories are created
    return resolved_path

def get_date_time():
    """ Returns the date and current time (`HH:MM`)."""
    date = datetime.now().strftime("%Y-%m-%d") # Format current time
    time = datetime.now().strftime("%H:%M") # Format current time
    return [date, time]

def get_time() -> str:
    """ Returns the current time with seconds (`HH:MM:SS`)."""
    time = datetime.now().strftime("%H:%M:%S") # Format current time
    return time

def substitute(text:str, substitutions:dict[str,str]) -> str:
    for word, sub in substitutions.items():
        text = text.replace(word, sub)
    return text

def get_prompt(path:str, substitutions:dict[str,str]) -> str:
    prompt = read_file(path)
    return substitute(prompt, substitutions)

def get_page_description(page:dict[str,str]) -> str:
    description = f"objective: \"{page['objective']}\""
    description += "\nskills:"
    for skill in page['skills']:
        description += f"\n- skill: \"{skill}\""
    return description

def sanitize_special_chars(input):
    """ Replace all repeated non-alphanumeric characters with underscores."""
    return re.sub(r"[^\w]+", "_", input)
