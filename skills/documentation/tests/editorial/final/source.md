# Line-counter fixture contract

Target version: fixture-v2. The tool is named `counter` in the CLI and glossary.
The sample command requires a repository checkout, a terminal and the checked-in
`tools/count-lines.sh` script. Its only input is the path to a readable UTF-8 text
file. For `samples/two-lines.txt`, stdout is `2`. For an empty file, stdout is `0`.
The documented invocation is `bash tools/count-lines.sh samples/two-lines.txt`.
The fixture provides no remote service, deployment command or performance data.
The selected page is an operational how-to for a maintainer who already knows
how to use a terminal. Place long explanations in a linked explanation page.
