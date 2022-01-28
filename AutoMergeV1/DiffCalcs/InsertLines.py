import difflib, re
from . import U

class InsertLines:
  def __init__(self) -> None:
    self.prefix = ""
    self.suffix = ""
    self.content = ""

  def __str__(self) -> str:
    lineCount = self.content.count("\n")

    if lineCount <= 1:
      return "insert " + self.content

    return (
      "insert " + str(lineCount) + 
      " line" + ("s" if lineCount > 1 else ""))
      
  def __repr__(self) -> str:
    return str(self)

  def applyTo(self, text : str) -> str:
    if self.prefix + self.suffix in text:

      text = text.replace(
        self.prefix + self.suffix,
        self.prefix + self.content + self.suffix,
        1)

      return text

    else:
      modifiedSearch, score = U.approximateSubStringByLine(
        self.prefix + self.suffix, text)

      if modifiedSearch is None: return text

      a = U.bestMatchSubdivisionByLine(
        self.prefix, self.suffix, text)

      lines = modifiedSearch.splitlines()

      mPrefix = "\n".join(lines[0:a]) + "\n"
      mSuffix = "\n".join(lines[a:]) + "\n"

      p1, p2, p3 = text.partition(modifiedSearch)

      return p1 + mPrefix + self.content + mSuffix + p3


  def cost(self):
    cost = len(self.content)

    if len(self.prefix) < 20: cost *= 2
    if len(self.suffix) < 20: cost *= 2

    return cost

def Process(old : str, new : str):
  o = old.splitlines()
  n = new.splitlines()

  s = difflib.SequenceMatcher(None, o, n).get_matching_blocks()
  s.append(difflib.Match(len(o), len(n), 1))

  for (cur, nex) in U.pairwise(s):
      
    if (cur.a + cur.size == nex.a and
        cur.b + cur.size < nex.b):
      # We've found an insertion

      stringInserted = "\n".join(n[cur.b + cur.size : nex.b ])
      stringInserted += "\n"

      # Don't insert whitespace in this diff tool.
      if stringInserted.strip() == "": continue

      insertedAfter = "\n".join(n[cur.b:cur.b + cur.size])
      insertedBefore = "\n".join(n[nex.b:nex.b + nex.size])

      while len(insertedAfter) > 180 and "\n" in insertedAfter:
        a,b,insertedAfter = insertedAfter.partition("\n")

      while len(insertedBefore) > 180 and "\n" in insertedBefore:
        insertedBefore,a,b = insertedBefore.rpartition("\n")

      if not insertedAfter.endswith("\n"): insertedAfter += "\n"

      diff = InsertLines()
      diff.content = stringInserted
      diff.prefix = insertedAfter
      diff.suffix = insertedBefore

      return diff
