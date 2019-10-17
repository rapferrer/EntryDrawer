# EntryDrawer

## Description
This is a basic python script I wrote to randomly select a winner in a competition involving number of entries

The script takes a .csv file as a command-line arg and then parses through it to generate an list containing the number of entries for each entrant listed in the file.

Finally, it uses `random` to select an index in that array to choose the winner.

Run it like:
`python randomselector.py file.txt`

## Ideas for Improvement
- ~~Account for csv files with OR without a header~~
- ~~Select multiple entrants in one pass through~~
    - ~~Do this by removing entrants after they are selected~~
    - ~~Or do this by ignoring previously selected entrants~~
- Adopt [PEP 257 docstring conventions](https://www.python.org/dev/peps/pep-0257/)
- ~Option for less verbose output~
    - ~Currently we print a lot. Good for verification but an option for only printing out some status text/the winner would be nice.~
- Create a GUI