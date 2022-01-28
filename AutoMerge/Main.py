import argparse, os, sys
import Merge, MergeSolver, MergeStrategies.GitResearch
import cProfile

parser = argparse.ArgumentParser(description='Auto merge')

parser.add_argument("merge_files", action="extend", nargs='*')

namespace = parser.parse_args(sys.argv[1:])

for mergeFile in namespace.merge_files:
  print("Working with", mergeFile)
  m = Merge.Merge()
  m.fromFile(mergeFile)

  if m.isValid == False: continue

  MergeStrategies.GitResearch.filePath = mergeFile

  result = MergeSolver.SolveMerge(m)

  if result is not None:
    with open(mergeFile, "w") as f:
      f.write(result)

  if False: pass