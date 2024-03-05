# Setup

To run you need to setup the Python virtual environment in the `.venv` folder. Navigate to [`src/`](src/) and use the following command to activate the environment:

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

## Folder structure

- [`prompts`](prompts/) - contains all prompts



## Running a single prompt (`generate.py`)

Generates questions for the given file.

A specific amount of questions can be provided as an optional argument, the default is `3`.

**NOTE: The file name is given without file ending. Input files (prompts) end in `.in` and outpus files (generated questions) end in `.out`, otherwise their names are identical.**

Example usage:

```
python generate.py examples/using_waitgroups
```

## Running all prompts in a folder (`generate_all.py`)

Generates questions for all prompts in a given directory.

**NOTE: The directory must end with a slash.**

Example usage:

```
python generate_all.py examples/
```
