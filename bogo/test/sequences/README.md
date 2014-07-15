This subdirectory holds scripts and resources to generate Vietnamese input
sequences for testing.

To use it, run:

    python gen.py

it will read `vi-DauCu.dic` file and generate `../DauCu.sequences` in this form:

> (key sequence):(corresponding Vietnamese word)

e.g:

> bieces:biếc

By default, it uses the dictionary with traditional mark position (dau cu), you
can instead make it generate sequences in the new style spelling by editing
`gen.py` and replace `vi-DauCu.dic` by `vi.dic`.
