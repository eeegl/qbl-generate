# QBL Question Generation

Here is the repo for running your prompts locally.

As it is now, for each new skill you have to copy the whole prompt and just replace the skill.

Create new folders as needed in `prompts` and `responses`.

## Folder structure

- [`.venv`](./.venv/) is the virtual environment for Python
    - Needs to be activated to run (see [Setup](#setup))
- [`prompts`](./prompts/) contains all prompts
    - [`promtps/examples`](./prompts/examples/) example prompts
- [`responses`](./responses/) contains all responses
    - [`responses/examples`](./responses/examples/) contains example responses
- [`src`](./src/) contains all Python files
    - [`__pycache__`](./src/generate_all.py) contains compiled binaries for faster execution (can be ignored)
    - [`generate_all.py`](./src/generate_all.py) generates responses for all prompts in a given folder
    - [`generate.py`](./src/generate.py) generates a response for a single given prompt
    - [`prompting.py`](./src/prompting.py) contains functions for interacting with the Chat Completions API
    - [`util.py`](./src/util.py) contains utility functions for reading and writing to files

## Setup

### OpenAI API key

Store your OpenAI API key in an environmental variable named `OPENAI_API_KEY_KTH`. This is retreived in the script using the `get_api_key()` in [`prompting.py`](./src/prompting.py).

### Virtual environment

To run you need to setup the Python virtual environment in the `.venv` folder. Navigate to [`src/`](./src/) and use the following command to activate the environment:

```bash
source .venv/bin/activate
```

You should then see a little `(.venv)` to the right in the CLI, like so:

```bash
(.venv) [orn:~/Documents/kth/da150x-kex/question-generation/src]%
```

The final step is to install the dependencies (only one) in [`requirements.txt`](requirements.txt). Do this by running:

```bash
pip install -r requirements.txt
```

After that you should be all set to run the script!



## Running a single prompt (`generate.py`)

> Make sure to activate the [virtual environment](#virtual-environment) first.

To generate a response for a single prompt, use:

```bash
python generate.py <file-path-without-ending> [<number-of-questions>]
```

This will generate a response for the prompt in `prompts/<file-path-without-ending>.in` and put the result in `responses/<file-path-without-ending>.out`.

If not specified, the default number of questions is `3`.

**NOTE: The file name is given without file ending. Input files (prompts) end in `.in` and outpus files (generated questions) end in `.out`, otherwise their names are identical.**

An example for [`prompts/examples/using_waitgroups.in`](./prompts/examples/using_waitgroups.in):

```bash
# 3 questions by default
python generate.py examples/using_waitgroups

# 5 questions
python generate.py examples/using_waitgroups 5
```



## Running all prompts in a folder (`generate_all.py`)

> Make sure to activate the [virtual environment](#virtual-environment) first.

To generate a response for a all prompts in a directory, use:

```bash
python generate.py <directory-path> [<number-of-questions>]
```

This will generate responses for all prompts in `prompts/<directory-path>` and put the results in `responses/<directory-path>`.

If not specified, the default number of questions is `3`.

**NOTE: The directory path must end with a slash.**

An example for [`prompts/examples/`](./prompts/examples/using_waitgroups.in):

```bash
# 3 questions by default
python generate.py examples/

# 5 questions
python generate.py examples/ 5
```
