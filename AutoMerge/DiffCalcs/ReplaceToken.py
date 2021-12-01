import difflib, re
from . import U

class ReplaceToken:
  """
  Represents a simple find and replace, done textually, respecting
  word boundaries.

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
  =

  =Old
  myOldApi->Function4(arg1, arg2)
  =New
  myNewApi->Function4(
    arg1, 
    arg2)
  =Summary
  Replace 'myOldApi' with 'myNewApi'
  =

  =Old
  // This is a com about how amaing autoMerge is
  // when calculating diffs.
  =New
  // This is a long comment about how amazing autoMerge is
  // when calculating diff's.
  =Summary
  Replace 'amaing' with 'amazing'
  =ApplyTo
  /* This is a coment about how  *
   * amaing autoMerge is         *
   * when calculating diffs.     */
  =Expect
  /* This is a coment about how  *
   * amazing autoMerge is         *
   * when calculating diffs.     */
  =# 
  Note that it should only replace one token - the longest, and it 
  doesn't correct the border of *'s here - that's in the decor lib.
  """
  def __init__(self) -> None:
    self.tr = {}

  def __str__(self) -> str:
    out = ""
    for (f, r) in self.tr.items():
      if r == "":
        out += "Remove '" + f + "'\n"
      else:
       out += "Replace '" + f + "' with '" + r + "'\n"

    return out.strip();

  def applyTo(self, text) -> str:

    for (f, r) in self.tr.items():
      text = re.sub(
        r"\b" + re.escape(f) + r"\b",
        r,
        text)
    return text

def Process(old : str, new : str):
  oT = re.findall(r"\b\w+\b",old)
  nT = re.findall(r"\b\w+\b",new)

  s = difflib.SequenceMatcher(None, oT, nT).get_matching_blocks()
  
  # We append 2 null matches at the start and end of the list, so
  # that we can iterate in pairs and get find token sequences between
  # matching sequences.
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
  rt.tr[biggestString] = fr[biggestString]
  return rt

