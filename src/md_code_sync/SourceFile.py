import sys
import logging


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
        file = open(file_path, "r")
        self.lines = file.readlines()
        file.close()
        self.chunks = {}

    def get(self, id):
        try:
            return self.chunks[id]
        except KeyError:
            logging.error(
                f"key {id} not found, available keys: {' '.join(self.chunks.keys())}")
            sys.exit(1)

    def get_chunk_id(self, line):
        return line.split(":")[1].strip().replace(")", "")

    def parse(self):
        collectors = []
        for line in self.lines:
            if "code_block_start:" in line:
                collectors.append(self.Collector(self.get_chunk_id(line)))
                continue
            if "code_block_end:" in line:
                for c in collectors:
                    if c.id == self.get_chunk_id(line):
                        self.chunks[self.get_chunk_id(line)] = c.finish()[1]
                continue
            for c in collectors:
                c.add_line(line)
