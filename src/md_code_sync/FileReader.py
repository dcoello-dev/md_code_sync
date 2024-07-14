from md_code_sync.SourceFile import SourceFile

class FileReader:
    def __init__(self, file_path:str, storage_path:str, write:bool):
        self.write_ = write
        self.file_path = file_path
        self.storage_path = storage_path
        file = open(file_path, "r")
        self.lines = file.readlines()
        file.close()
        self.links = []

    def parse_link(self, lines, index):
        arguments = lines[index].split("code_block_link:")[
            1].replace(")", "")
        arguments = ' '.join(arguments.split()).split(" ")
        ret = dict()
        for arg in arguments:
            k, v = arg.split(":")
            ret[k.strip()] = v.strip()

        ret["ext"] = ret["file"].split(".")[1]
        
        if index + 1 == len(lines) :
            lines.append("")
        ret["linked"] = (f"```{ret['ext']}" in lines[index+1])
        return ret

    def parse(self):
        self.links = []
        for i, line in enumerate(self.lines):
            if "code_block_link:" in line:
                link = self.parse_link(self.lines, i)
                link["line"] = i
                self.links.append(link)

    def get_source_files(self):
        source_files = []
        for l in self.links:
            source_files.append(l["file"])
        return set(source_files)

    def reset(self):
        lines = []
        flag = True
        for i,l in enumerate(self.lines):
            if "```" in l and "code_block_link:" in self.lines[i-1]:
                flag = False
            if flag:
                lines.append(l)
            if not flag and "```\n" in l:
                flag = True
 
        f = open(self.file_path, "w")
        self.lines = lines
        f.write("".join(self.lines))
        
    def __output(self, content):
        if self.write_:
            f = open(self.file_path, "w")
            f.write(content)
        else:
            print(content)


    def link(self):
        sources = {}
        for f in self.get_source_files():
            sources[f] = SourceFile(self.storage_path+ "/" + f)
            sources[f].parse()
        
        ret = ""
        for i, l in enumerate(self.links):
            ret += "".join(self.lines[0 if i ==
                           0 else self.links[i-1]["line"]+1:int(l["line"])+1])
            ret += f"```{l['ext']}\n"
            ret += sources[l["file"]].get(l["id"])
            ret += "```\n"
        s = 0 if len(self.links) == 0 else self.links[-1]["line"] + 1
        ret += "".join(self.lines[s:])

        self.__output(ret)

