
import DiffCalcs
import pkgutil
import textwrap
import DiffSolver
import os

from DiffCalcs import ReplaceToken as t

print("""
Running all DiffCalc unit tests:
""")

def runDiffTests(string, process):
  for run in ("\n" + string).split("\n=")[1:]:
    if len(run.strip()) == 0: continue
    (token, string) = run.split("\n",1)

    token = token.strip()

    if token == "Old":
      old = string

    elif token == "New":
      new = string

    elif token == "Summary":
      actualSummary = str(process(old, new))
      expectedSummary = string
      print("old:\n" + old)
      print("new:\n" + new)
      print("summary:\n" + actualSummary)

      assert(actualSummary.strip() == expectedSummary.strip())

    elif token == "ApplyTo":
      diff = process(old, new)
      appliedResult = diff.applyTo(string)

    elif token == "Expect":
      expectedResult = string

      print("applied to:\n" + appliedResult)
      print("new:\n" + expectedResult)

      assert(appliedResult == expectedResult)

    elif token == "#": continue
    else:
      raise

# 
# First run the tests over all the in module documentation - using
# Only the Process method in each module.
#
for a in pkgutil.iter_modules(['DiffCalcs']):
  if a.name == "U": continue

  print(a.name)

  exec("from DiffCalcs import " + a.name + " as t")

  doco = t.__dict__[a.name].__doc__

  if doco is None: continue

  doco = textwrap.dedent(doco).strip()

#  runDiffTests(doco, t.Process)

# 
# Second - run tests over the entire library.
#

testFolder =  os.path.join(os.path.dirname(__file__), 'DiffTests')

for filename in os.listdir(testFolder):
  c = open(os.path.join(testFolder, filename)).read()

  def solve(a,b):
    sequences = DiffSolver.AllPossibleSolutions(a,b)
    return sequences[0]

  runDiffTests(c, solve)

