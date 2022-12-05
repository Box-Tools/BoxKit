import sys


def get_build_base():

    build_base_long = [
        arg[12:].strip("= ") for arg in sys.argv if arg.startswith("--build-base")
    ]
    build_base_short = [arg[2:].strip(" ") for arg in sys.argv if arg.startswith("-b")]
    build_base_arg = build_base_long or build_base_short
    if build_base_arg:
        build_base = build_base_arg[0]
    else:
        build_base = "."

    return build_base
