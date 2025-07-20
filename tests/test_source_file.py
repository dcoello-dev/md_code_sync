import sys

from md_code_sync.SourceFile import SourceFile

sys.path.append("../")


CONTENT = "content"

SINGLE_LINK = """
/// code_block_start: INCLUDE
#include <iostream>
/// code_block_end: INCLUDE
"""

COMPLETE_FILE = """
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
"""


def test_source_file_content(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=CONTENT))
    sf = SourceFile("fakepath")
    assert len(sf.lines) == 1
    assert sf.lines[0] == CONTENT


def test_source_file_single_link(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=SINGLE_LINK))
    sf = SourceFile("fakepath")
    sf.parse()
    assert len(sf.chunks) == 1
    assert sf.get("INCLUDE") == "#include <iostream>\n"
