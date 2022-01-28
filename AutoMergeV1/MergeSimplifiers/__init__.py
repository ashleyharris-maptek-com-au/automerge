"""
MergeSimplifiers are useful tools to transform an unsolvable merge
into a solvable one.

These may involve:
- splitting a big merge into smaller merges.
- partitioning the merge into decorated and undecorated
- partially applying bits of the merge.
- Extracting equal chunks out of the merge.
"""

import pkgutil
import pathlib
import sys, os
folderPath = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(folderPath)

allMergeSimplifiers = []

for a in pkgutil.iter_modules([ os.path.join(folderPath, 'MergeSimplifiers')]):
  exec("from MergeSimplifiers import " + a.name + " as t")

  if "Process" in dir(t):
    allMergeSimplifiers.append(t.Process)

