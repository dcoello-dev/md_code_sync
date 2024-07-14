# md_code_sync

tool to inject code snippets from source code files on markdown files.

reference your code from your markdown documentation without have to worry to maintain it in code blocks and source files, just write your code in your source files and inject it into your markdown documentation.

## usage

there are 3 keywords:

- code_block_link : used on markdown file that wants to add a new code block from a different file.
- code_block_start : used on source file to indicate where a new snippet starts.
- code_block_end : where code block ends.

### code_block_link

place a comment in your markdown file that references the source file and the id of the snippet you want to link:

```markdown
[//]: # (code_block_link: file:doc/example/example.cpp id:LINK_EXAMPLE)
```

it accepts two arguments:
- file: relative path from input markdown file or from root dir if given.
- id: id of the code snippet on this file.

### code_block_start/end

place this directives on source file to identify snippets:

```cpp
/// code_block_start: MAIN
int main(void) {
  std::cout << "hello world" << std::endl;
  return 0;
}
/// code_block_end: MAIN
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
