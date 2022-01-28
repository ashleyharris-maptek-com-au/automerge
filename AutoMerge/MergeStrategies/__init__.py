
import pkgutil
import pathlib
import sys, os
folderPath = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(folderPath)

allStrategies = []

for a in pkgutil.iter_modules([os.path.join(folderPath,'MergeStrategies')]):
  exec("from MergeStrategies import " + a.name + " as t")

  if "Solve" in dir(t):
    allStrategies.append(t.Solve)

