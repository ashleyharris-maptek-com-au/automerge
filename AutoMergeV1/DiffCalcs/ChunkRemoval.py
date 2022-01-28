import difflib, re
from . import U

class ChunkRemoval:
  def __init__(self) -> None:
    self.chunks = []

  def __str__(self) -> str:
    out = ""
    for chunk in self.chunks:
      out += "Remove large chunk of code: '" + chunk[0:40] + "..." + chunk[-10:-1] + "\n"

    return out

  def __repr__(self) -> str:
    return str(self)

  def applyTo(self, text : str) -> str:
    for chunk in self.chunks:
      match, score = U.approximateSubStringByLine(chunk, text)
      if match is not None:
        text = text.replace(match, "")

    text = re.sub(r"\n\n+","\n\n", text)

    text = text.rstrip()

    return text

  def cost(self):
    cost = 0
    for chunk in self.chunks:
      cost += chunk.count("\n")
    return cost

class Chunk:
  def __init__(self) -> None:
    self.origChunk = ""
    self.actChunk = ""
    self.offset = 0
    self.found = False

def Process(old : str, new : str):

  chunks = []

  for s in old.split("\n\n"):
    c = Chunk()
    c.origChunk = s
    
    result, score = U.approximateSubStringByLine(s, new)

    if result is not None:
      c.found = True
      c.actChunk = result
      c.offset = new.index(result)

    chunks.append(c)

  cr = ChunkRemoval()
  
  # First - go through and find all runs of missing chunks
  curChunk = ""
  for c in chunks:
    if c.found == False:
      if curChunk != "": curChunk += "\n\n"
      curChunk += c.origChunk
    else:
      if curChunk != "": cr.chunks.append(curChunk)
      curChunk = ""
  if curChunk != "":
    cr.chunks.append(curChunk)

  if len(cr.chunks) > 0 : return cr
  return None

  """
  cOld = old.split("\n\n")
  ret = ChunkRemoval()

  while True:
    bestScore = 0
    bestMatch = None
    bestC = ""

    for c in cOld:
      if c.strip() == "": continue

      if c in new:
        bestScore = 1.0
        bestMatch = c
        bestC = c
        break

      match, score = U.approximateSubStringByLine(c, new)

      if score > bestScore:
        bestScore = score
        bestMatch = match
        bestC = c

    if bestMatch is not None:
      cOld.remove(bestC)
      new = new.replace(bestMatch, "")

    if bestMatch is None: break
    if len(cOld) == 0: break
    if new.count("\n") < 5: break

  ret.chunks = cOld
  if len(ret.chunks) == 0: return None
  if len(ret.chunks[0]) == 0 and len(ret.chunks) == 1: return None

  return ret
"""