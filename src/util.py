import os
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
