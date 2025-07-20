import logging
import subprocess
import sys

from md_code_sync.SourceFile import SourceFile


class FileReader:
    def __init__(self, file_path: str, storage_path: str, write: bool):
        self.write_ = write
        self.file_path = file_path
        self.storage_path = storage_path
        with open(file_path, "r") as file:
            self.lines = file.readlines()
        self.links = []
        self.exes = []

    def parse_link(self, lines, index):
        arguments = lines[index].split("code_block_link:")[1].replace(")", "")
        arguments = " ".join(arguments.split()).split(" ")
        ret = dict()
        for arg in arguments:
            try:
                k, v = arg.split(":")
                ret[k.strip()] = v.strip()
            except ValueError:
                print(f"{self.file_path}: error on link {lines[index]}")
                sys.exit(1)

        ret["ext"] = ret["file"].split(".")[1]

        if index + 1 == len(lines):
            lines.append("")
        ret["linked"] = f"```{ret['ext']}" in lines[index + 1]
        return ret

    def parse_exe(self, lines, index):
        arguments = lines[index].split("md_block_exe:")[1].replace(")", "")
        chunks = arguments.split(":")
        ret = dict()

        if len(chunks) > 1:
            for i in range(0, len(chunks) - 2):
                ret[chunks[i].split(" ")[-1]] = " ".join(
                    chunks[i + 1].split(" ")[:-1]
                )

        ret[chunks[-2].split(" ")[-1]] = chunks[-1][:-1]

        if index + 1 == len(lines):
            lines.append("")

        return ret

    def parse(self):
        """identify links"""
        logging.info(f"{self.file_path} parsing links")
        self.links = []
        for i, line in enumerate(self.lines):
            if "code_block_link:" in line:
                link = self.parse_link(self.lines, i)
                link["line"] = i
                self.links.append(link)
                logging.info(f"{self.file_path}:{i} added link")
            if "md_block_exe:" in line:
                exe = self.parse_exe(self.lines, i)
                exe["line"] = i
                self.exes.append(exe)
                logging.info(f"{self.file_path}:{i} added exe")

    def get_source_files(self):
        source_files = []
        for link in self.links:
            source_files.append(link["file"])
        return set(source_files)

    def reset(self):
        """reset source code links"""
        logging.info(f"{self.file_path} reseting links")
        lines = []
        flag_link = True
        flag_exe = True
        for i, l in enumerate(self.lines):
            if "```" in l and "code_block_link:" in self.lines[i - 1]:
                flag_link = False
                continue
            if "[//]: ####" in l and "md_block_exe:" in self.lines[i - 1]:
                flag_exe = False
                continue
            if flag_link and flag_exe:
                lines.append(l)
                continue
            if not flag_link and "```\n" in l:
                flag_link = True
                continue
            if not flag_exe and "[//]: ####" in l:
                flag_exe = True
                continue

        self.lines = lines

        if self.write_:
            f = open(self.file_path, "w")
            f.write("".join(self.lines))

    def output(self):
        content = "\n".join(self.lines)
        if self.write_:
            f = open(self.file_path, "w")
            f.write(content)
        else:
            print(content)

    def link(self):
        sources = {}
        for f in self.get_source_files():
            sources[f] = SourceFile(self.storage_path + "/" + f)
            sources[f].parse()

        ret = ""
        for i, link in enumerate(self.links):
            ret += "".join(
                self.lines[
                    (
                        0 if i == 0 else self.links[i - 1]["line"] + 1
                    ) : int(  # noqa
                        link["line"]
                    )
                    + 1
                ]
            )
            ret += f"```{link['ext']}\n"
            ret += sources[link["file"]].get(link["id"])
            ret += "```\n"
        s = 0 if len(self.links) == 0 else self.links[-1]["line"] + 1
        ret += "".join(self.lines[s:])

        self.lines = [f"{link}\n" for link in ret.split("\n")]

    def exe(self):
        ret = ""
        for i, cmd in enumerate(self.exes):
            ret += "".join(
                self.lines[
                    (
                        0 if i == 0 else self.exes[i - 1]["line"] + 1
                    ) : int(  # noqa
                        cmd["line"]
                    )
                    + 1
                ]
            )
            ret += "[//]: ####\n"
            if "wrap" in self.exes[i].keys():
                ret += f'```{self.exes[i]["wrap"]}\n'

            result = subprocess.Popen(
                cmd["exe"].split(" "),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, _ = result.communicate()
            ret += out.decode("utf-8")
            if "wrap" in self.exes[i].keys():
                ret += "```\n"
            ret += "\n[//]: ####\n"

        s = 0 if len(self.exes) == 0 else self.exes[-1]["line"] + 1
        ret += "".join(self.lines[s:])

        self.lines = [f"{ex}" for ex in ret.split("\n")]
