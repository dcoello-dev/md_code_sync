import argparse
import logging
import os
import sys

from md_code_sync.FileReader import FileReader

parser = argparse.ArgumentParser(
    description="Sync code blocks of markdown and source files"
)

parser.add_argument(
    "md_file", nargs=argparse.REMAINDER, help="input markdown files"
)

parser.add_argument(
    "-v",
    "--verbose",
    choices=["VERBOSE", "DEBUG", "INFO", "WARNING", "ERROR"],
    default="ERROR",
    help="output log level",
)

parser.add_argument(
    "-r",
    "--root_dir",
    default="",
    help="by default tool assumes relative \
    paths are from markdown file folder, \
    if you set this argument tool will assume \
    relative links will be from root dir",
)

parser.add_argument(
    "-w",
    "--write",
    action="store_true",
    default=False,
    help="write in place, if not set tool will output to stdout",
)

args = parser.parse_args()

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=eval(f"logging.{args.verbose.upper()}"),
)


def main():
    logging.debug(f"processing {str(args.md_file)}")
    for file in args.md_file:
        if args.root_dir == "":
            root_dir = "/".join(os.path.abspath(file).split("/")[:-1])
        else:
            root_dir = args.root_dir
        logging.debug(f"root dir {root_dir}")
        reader = FileReader(file, root_dir, args.write)
        reader.reset()
        reader.parse()
        reader.link()
        reader.exe()
        reader.output()

    sys.exit(0)


if __name__ == "__main__":
    # if there is not user root dir set md file dir as root dir
    main()
