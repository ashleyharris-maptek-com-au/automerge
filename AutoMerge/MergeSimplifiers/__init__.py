"""
MergeSimplifiers are useful tools to transform an unsolvable merge
into a solvable one.

These may involve:
- splitting a big merge into smaller merges.
- partitioning the merge into decorated and undecorated
- partially applying bits of the merge.
- Extracting equal chunks out of the merge.
"""