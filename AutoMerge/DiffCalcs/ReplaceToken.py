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

  def cost(self):
    cost = 0
    for (f, r) in self.tr.items():
      cost += len(f)
      cost += len(r)

      # If we're replacing a tiny string, make this more costly,
      # as that makes it more risky.
      if len(f) < 5: cost *= 2
      if len(f) <= 2: cost *= 2
    return cost

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
    elif (nex.a - cur.a - cur.size > 0 and 
          nex.a - cur.a - cur.size == nex.b - cur.b - cur.size):
      # This is a sequence of tokens that have changed - this is a bit more risky
      # as any sequence of words can theoretically match:
      # "Renderer->Draw(Object.Handle)" and "std::cout << std::endl" - Match?
      #
      # To solve - we look at the non-whitespace between the tokens, if that
      # matches - we consider the token replaced. 

      oldPattern = r"\b" + re.escape(oT[cur.a + cur.size]) + r"\b(.+?)\b"
      oldPattern += r"\b" + re.escape(oT[cur.a + cur.size + 1]) + r"\b"

      if nex.a > 0:
        oldPattern = (
          r"\b" + re.escape(oT[cur.a + cur.size-1]) + r"\b(.+?)\b" +
          oldPattern)
      else:
        oldPattern += r"(.+?)\b" + re.escape(oT[cur.a + cur.size + 2]) + r"\b"

      pattern = re.compile(oldPattern, re.DOTALL)

      oldM = re.findall(pattern, old)
      newM = re.findall(pattern, new)

      if len(oldM) == 1 and len(newM) == 0:

        newPattern = r"\b" + re.escape(nT[cur.b + cur.size]) + r"\b(.+?)\b"
        newPattern += r"\b" + re.escape(nT[cur.b + cur.size + 1]) + r"\b"

        if nex.b > 0:
          newPattern = (
            r"\b" + re.escape(oT[cur.b + cur.size-1]) + r"\b(.+?)\b" +
            newPattern)
        else:
          newPattern += r"(.+?)\b" + re.escape(oT[cur.b + cur.size + 2]) + r"\b"

        pattern2 = re.compile(newPattern, re.DOTALL)

        oldM2 = re.findall(pattern2, old)
        newM2 = re.findall(pattern2, new)

        if len(oldM2) == 0 and len(newM2) == 1:
          between1a = oldM[0][0].strip()
          between2a = newM2[0][0].strip()

          between1b = oldM[0][1].strip()
          between2b = newM2[0][1].strip()

          if between1a == between2a and between1b == between2b:
            f = oT[cur.a + cur.size]
            r = nT[cur.b + cur.size]

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

