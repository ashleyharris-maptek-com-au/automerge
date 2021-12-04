import difflib, re
from . import U

class StringReplacement:
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
        f,
        r,
        text)
    return text

def Process(old : str, new : str):
  s = difflib.SequenceMatcher(None, old, new).get_matching_blocks()
  
  # We append 2 null matches at the start and end of the list, so
  # that we can iterate in pairs and get find token sequences between
  # matching sequences.
  s.insert(0, difflib.Match(-1, -1, 0))
  #s.append(difflib.Match(len(old), len(new), 0))

  confirmedFr = {}
  disprovedFr = {}

  fr = {}

  while len(s) > 3:

    for (cur, nex) in U.pairwise(s):
      if cur.size == 0: continue

      endOfA = cur.a + cur.size
      endOfB = cur.b + cur.size

      f = old[endOfA:nex.a]
      r = new[endOfB:nex.b]

      if len(f) == 0: continue

      f = re.sub(r"\s+", " ", f)

      f = re.escape(f)
      f = f.replace(" ", r"\s+")

      q = re.compile(f)

      mfoCount = len(re.findall(q, old))
      mfnCount = len(re.findall(q, new))

      if mfoCount > 0 and mfnCount == 0:
        if f in fr:
          # Duplicate find
          if fr[f] == r:
            # It keeps the same f->r
            confirmedFr[f] = 1
            continue
          else:
            disprovedFr[f] = 1
            del confirmedFr[f]
            del fr[f]

        fr[f] = r

    smallestMatch = min((x for x in s if x.size > 0), key = lambda x : x.size)
    s.remove(smallestMatch)

  if len(fr) == 0: return None

  if len(confirmedFr):
    bestKey = max(confirmedFr.keys(), key = lambda x : len(x))
  else:
    bestKey = max(fr.keys(), key = lambda x : len(x))

  z = StringReplacement()
  z.tr[bestKey] = fr[bestKey]

  return z