import argparse

#option argument
def get_arg():
    parser = argparse.ArgumentParser(description='argparse sample.')
    #bool option
    parser.add_argument('-f','--follow', action='store_true', default=False, help='follow the hierarchy (default: Not follow the hierarchy)')
    return parser.parse_args()