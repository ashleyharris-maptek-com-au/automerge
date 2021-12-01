
import DiffCalcs
import pkgutil
import textwrap

from DiffCalcs import ReplaceToken as t

print("""
Running all DiffCalc unit tests:
""")

for a in pkgutil.iter_modules(['DiffCalcs']):
  if a.name == "U": continue

  print(a.name)

  exec("from DiffCalcs import " + a.name + " as t")

  doco = textwrap.dedent(
    t.__dict__[a.name].__doc__).strip()

  for run in doco.split("\n=")[1:]:
    if len(run.strip()) == 0: continue
    (token, string) = run.split("\n",1)

    token = token.strip()

    if token == "Old":
      old = string
    elif token == "New":
      new = string
    elif token == "Summary":
      actualSummary = str(t.Process(old, new))
      expectedSummary = string
      assert(actualSummary == expectedSummary)
      print("old:\n" + old)
      print("new:\n" + new)
      print("summary:\n" + actualSummary)
    elif token == "ApplyTo":
      diff = t.Process(old, new)
      appliedResult = diff.applyTo(string)
    elif token == "Expect":
      expectedResult = string
      assert(appliedResult == expectedResult)
      print("applied to:\n" + appliedResult)
      print("new:\n" + expectedResult)
    elif token == "#": continue
    else:
      raise
