import sys, os
from setup import setup
from prompting import generate_questions

if __name__ == "__main__":
    config, skillmap = setup()

    # print("SKILLMAP:", skillmap)
    # print("ARGS:", args)

    # Actual question generation
    try:

        generate_questions(config, skillmap)
    except Exception as e:
        # raise e # Uncomment for more verbose errors
        print(e)
        sys.exit(1)
