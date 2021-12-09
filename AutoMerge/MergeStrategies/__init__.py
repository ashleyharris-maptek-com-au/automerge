
import pkgutil

allStrategies = []

for a in pkgutil.iter_modules(['MergeStrategies']):
  exec("from MergeStrategies import " + a.name + " as t")

  if "Solve" in dir(t):
    allStrategies.append(t.Solve)

