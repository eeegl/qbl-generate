import os, sys
from prompting import generate_questions

if __name__ == "__main__":
    args        = sys.argv
    min_args    = 2 # Used for CLI input validation
    script_name = args[0]

    # Defaults, set as required
    num_questions = 3
    prompts_dir   = "../prompts/"   # Use "" to specify custom
    responses_dir = "../responses/" # directories from CLI

    if len(args) < min_args:
        # Validate CLI input
        raise ValueError("Too few arguments. Usage: "
                         + script_name + " <file-name> [<number-of-questions>]")
    
    # Gets file paths from CLI
    file_name = args[1]

    # Constructs the full paths
    # Note the use of '.in' for prompts and '.out' for responses
    prompt_path = os.path.join(prompts_dir, file_name + ".in")
    response_path = os.path.join(responses_dir, file_name + ".out")

    if len(args) > min_args: 
        # User specified number of questions, so update
        num_questions = args[2]

    # Actual question generation
    try:
        generate_questions(prompt_path, response_path, num_questions)
    except Exception as e:
        # raise e # Uncomment for more verbose errors
        print(e)
        sys.exit(1)
