from Merge import Merge
import MergeSimplifiers
import MergeStrategies
import itertools

def SolveMerge(m : Merge):
  
  merge = m
  while True:
    anyChange = False
    for ms in MergeSimplifiers.allMergeSimplifiers:
      m2 = ms(merge)
      if m2:
        merge = m2
        anyChange = True
    if anyChange == False: break

  allResults = {}  
  for solve in MergeStrategies.allStrategies:
    results = solve(merge)
    allResults.update(results)

  q = max(allResults, key=allResults.get)
  return q

m = Merge()
m.fromString("""
<<<<<<<
    Tstring i = "";
|||||||
    std::vector<sysC_Path> destinations = {expectedImage};
    Tstring i = "";
=======
    std::vector<sysC_Path> destinations = {expectedImage};
    Tstring i = "a";
>>>>>>>
""")

SolveMerge(m)

