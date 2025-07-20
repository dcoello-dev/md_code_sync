import logging
import sys


class SourceFile:
    class Collector:
        def __init__(self, id):
            self.id = id
            self.source = ""

        def add_line(self, line):
            self.source += line

        def finish(self):
            return (id, self.source)

    def __init__(self, file_path):
        with open(file_path, "r") as file:
            self.lines = file.readlines()
        self.chunks = {}

    def parse(self):
        collectors = []
        for line in self.lines:
            if "code_block_start:" in line:
                collectors.append(self.Collector(self.__get_chunk_id(line)))
                continue
            if "code_block_end:" in line:
                for c in collectors:
                    if c.id == self.__get_chunk_id(line):
                        self.chunks[self.__get_chunk_id(line)] = c.finish()[1]
                continue
            for c in collectors:
                c.add_line(line)

    def get(self, id):
        try:
            return self.chunks[id]
        except KeyError:
            logging.error(
                f"key {id} not found,"
                + f"available keys: {' '.join(self.chunks.keys())}"
            )
            sys.exit(1)

    def __get_chunk_id(self, line):
        return line.split(":")[1].strip().replace(")", "")
