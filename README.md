# EntryDrawer

## Description

This is a basic python script I wrote to randomly select a winner in a drawing from different entrants each with their own number of entries.

The script takes a .csv or .json file as a command-line arg, parses through it to generate an collection of entrants, then randomly selects an entry number and returns the winner with that number. It can also repeat the selection process for multiple winners/drawings.

Run it like:
`python randomselector.py file.[csv, json]`
Or:
`./randomselector.py file.csv`
