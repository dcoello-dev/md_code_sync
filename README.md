# md_code_sync

tool to inject code snippets from source code files on markdown files.

reference your code from your markdown documentation without have to worry to maintain it in code blocks and source files, just write your code in your source files and inject it into your markdown documentation.

[//]: # (md_block_exe: exe:cloc -md ./src/md_code_sync/)
[//]: ####
cloc|github.com/AlDanial/cloc v 1.98  T=0.01 s (448.8 files/s, 41585.5 lines/s)
--- | ---

Language|files|blank|comment|code
:-------|-------:|-------:|-------:|-------:
Python|3|44|3|231
--------|--------|--------|--------|--------
SUM:|3|44|3|231

[//]: ####


## usage

[//]: # (md_block_exe: exe:md_code_sync --help wrap:bash)
[//]: ####
```bash
usage: md_code_sync [-h] -i MD_FILE [-r ROOT_DIR] [-w]

Sync code blocks of markdown and source files

options:
  -h, --help            show this help message and exit
  -i MD_FILE, --md_file MD_FILE
                        inpunt markdown file
  -r ROOT_DIR, --root_dir ROOT_DIR
                        by default tool assumes relative paths are from
                        markdown file folder, if you set this argument tool
                        will assume relative links will be from root dir
  -w, --write           write in place, if not set tool will output to stdout
```

[//]: ####

there are 3 keywords:

- **codeblock_link:** used on markdown file that wants to add a new code block from a different file.
- **codeblock_start:** used on source file to indicate where a new snippet starts.
- **codeblock_end:** where code block ends.

> [!NOTE]
> Replace `codeblock` by `code_block` necessary to avoid conflicts parsing this file

### code_block_link

place a comment in your markdown file that references the source file and the id of the snippet you want to link:

```markdown
[//]: # (code_block_link: file:doc/example/example.cpp id:ALL)
```cpp
#include <iostream>

int main(void) {
  std::cout << "hello world" << std::endl;
  return 0;
}
```

this directives can be nested:

```cpp
/// code_block_start: ALL
/// code_block_start: INCLUDE
#include <iostream>
/// code_block_end: INCLUDE

/// code_block_start: MAIN
int main(void) {
  std::cout << "hello world" << std::endl;
  return 0;
}
/// code_block_end: MAIN
/// code_block_end: ALL
```

nested directives will not be shown on linked codeblock.


## example

```bash
python3 -m md_code_sync -i doc/example/doc.md
```
