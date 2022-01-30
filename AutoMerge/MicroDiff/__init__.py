"""
MicroDiffs are small, localised changes to a chunk of text.

These include things like:
- A token has changed.
- 2 tokens have swapped position
- Indentation has increased
- A string has been found/replaced
- A string was inserted between 2 tokens
- 2 lines have swapped

etc.

Microdiffs analysis uses O(N^lots) algorithms, and should never be run over more
than about 5 lines of text, or run over text that is radically different. Use 
MegaDiffs to narrow down the scope and find similar regions.


"""

