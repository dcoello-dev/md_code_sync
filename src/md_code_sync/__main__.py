import argparse

from md_code_sync.FileReader import FileReader

parser = argparse.ArgumentParser(
    description="Sync code blocks of markdown and source files")

parser.add_argument(
    '-i', '--md_file',
    required=True,
    help="inpunt markdown file")

parser.add_argument(
    '-r', '--root_dir',
    default="",
    help="by default tool assumes relative paths are from markdown file folder, \
    if you set this argument tool will assume relative links will be from root dir")

parser.add_argument(
    '-w', '--write',
    action='store_true',
    default=False,
    help="write in place, if not set tool will output to stdout")

args = parser.parse_args()

if __name__ == "__main__":
    if args.root_dir == "":
        args.root_dir = "/".join(args.md_file.split("/")[:-1])
    reader = FileReader(args.md_file, args.root_dir, args.write)
    reader.parse()
    reader.reset()
    reader.parse()
    reader.link()
