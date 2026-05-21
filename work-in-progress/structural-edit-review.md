agent generated some bad comby syntax.
review both comby and semgrep reference documents.

have the agent try with some real code to confirm syntax,etc.

e.g. it tried -lang cpp (which is not valid, it only appears to have C and the aprameter is -lang .c)
it also passed multiple `-d` which is not valid, it only accepts one.

call the comby --help  command, and check online.

same for semgrep

