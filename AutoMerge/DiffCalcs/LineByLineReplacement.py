import difflib, re
from . import U

class LineByLineReplacement:
  def __init__(self) -> None:
    self.prefix = ""
    self.suffix = ""
    self.oldContent = ""
    self.newContent = ""

  def __str__(self) -> str:
    lineCount = self.oldContent.count("\n") + self.newContent.count("\n")

    if lineCount <= 2:
      return "Modify a line"

    return (
      "Replace " + str(lineCount) + 
      " line" + ("s" if lineCount > 1 else ""))
      
  def __repr__(self) -> str:
    return str(self)

  def applyTo(self, text : str) -> str:
    rawSearch = self.prefix + self.oldContent + self.suffix

    if rawSearch in text:

      text = text.replace(
        rawSearch,
        self.prefix + self.newContent + self.suffix,
        1)

      return text

    else:
      
      modifiedSearch, score = U.approximateSubStringByLine(rawSearch, text)

      if modifiedSearch is None: return text

      a,b = U.bestMatchTripleSubdivisionByLine(
        self.prefix, self.oldContent, self.suffix, modifiedSearch)

      lines = modifiedSearch.splitlines()

      mPrefix = "\n".join(lines[0:a]) + "\n"
      mFind = "\n".join(lines[a:b]) + "\n"
      mSuffix = "\n".join(lines[b:]) + "\n"

      p1, p2, p3 = text.partition(modifiedSearch)

      return p1 + mPrefix + self.newContent + mSuffix + p3



  def cost(self):
    cost = len(self.oldContent)
    cost *= len(self.newContent)

    if len(self.prefix) < 20: cost *= 2
    if len(self.suffix) < 20: cost *= 2

    return cost

def Process(old : str, new : str):
  o = old.splitlines()
  n = new.splitlines()

  s = difflib.SequenceMatcher(None, o, n).get_matching_blocks()
  s.append(difflib.Match(len(o), len(n), 1))

  for (cur, nex) in U.pairwise(s):
      
    if (cur.a + cur.size != nex.a and
        cur.b + cur.size != nex.b):
      # We've found a replacement

      stringFound = "\n".join(o[cur.a + cur.size : nex.a ])
      stringFound += "\n"

      stringReplaced = "\n".join(n[cur.b + cur.size : nex.b ])
      stringReplaced += "\n"

      insertedAfter = "\n".join(n[cur.b:cur.b + cur.size])
      insertedBefore = "\n".join(n[nex.b:nex.b + nex.size])

      while len(insertedAfter) > 100 and "\n" in insertedAfter:
        a,b,insertedAfter = insertedAfter.partition("\n")

      while len(insertedBefore) > 100 and "\n" in insertedBefore:
        insertedBefore,a,b = insertedBefore.rpartition("\n")

      if not insertedAfter.endswith("\n"): insertedAfter += "\n"

      diff = LineByLineReplacement()
      diff.oldContent = stringFound
      diff.newContent = stringReplaced
      diff.prefix = insertedAfter
      diff.suffix = insertedBefore

      return diff
