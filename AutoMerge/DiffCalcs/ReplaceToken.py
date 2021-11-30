import difflib, re
from . import U

class ReplaceToken:
  """
  Represents a simple find and replace, done textually.



  =Old
  This is a simple example.
  =New
  This was a simple example.
  =Summary
  Replace 'is' with 'was'
  =ApplyTo
  This is a simple example!
  =Expect
  This was a simple example!
  """
  def __init__(self) -> None:
    self.find = None
    self.replace = None

  def __str__(self) -> str:
    if self.find is None: return ""
    if self.replace == "":
      return "Remove '" + self.find + "'"
    return "Replace '" + self.find + "' with '" + self.replace + "'"

  def applyTo(self, old) -> str:
    return re.sub(
      r"\b" + re.escape(self.find) + r"\b",
      self.replace,
      old)

def Process(old : str, new : str) -> [ReplaceToken, None]
  oT = old.split()
  nT = new.split()

  s = difflib.SequenceMatcher(None, oT, nT).get_matching_blocks()
  
  s.insert(0, difflib.Match(-1, -1, 1))
  s.append(difflib.Match(len(oT), len(nT), 1))

  fr = {}

  for (cur, nex) in U.pairwise(s):
    # Start with the trivial 1->1 token replacement
    if (cur.a + cur.size + 1 == nex.a and
        cur.b + cur.size + 1 == nex.b):
      # oooh we've got a thing found and replaced.
      f = oT[nex.a - 1]
      r = nT[nex.b - 1]

      fr[f] = r

  if len(fr) == 0:
    return None

  biggestString = ""

  for (f, r) in fr.items():
    findCount = len(re.findall(r"\b" + re.escape(f) + r"\b", old))

    if r == "":
      if (len(f) > len(biggestString)): biggestString = f
      continue

    replaceCount = len(re.findall(r"\b" + re.escape(r) + r"\b", new))
    ignoreCount = len(re.findall(r"\b" + re.escape(r) + r"\b", old))

    if (findCount + ignoreCount == replaceCount):
      if (len(f) > len(biggestString)): biggestString = f
      continue



  if biggestString == "": return None

  rt = ReplaceToken()
  rt.find = biggestString
  rt.replace = fr[biggestString]
  return rt

