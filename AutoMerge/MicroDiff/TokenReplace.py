
"""
=# 

Represents the replacement of a token, or token sequence, with
another token or token sequence

=Old
#ifdef WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif // WINDOWS
=New
#ifdef COMPILE_FOR_WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif // COMPILE_FOR_WINDOWS
=Expect
Token replacement: 'WINDOWS' -> 'COMPILE_FOR_WINDOWS'
"""

import re

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

neightbourRegex = r"([^\w\s]*)"

class ReplaceToken:
  def __init__(self) -> None:
    self.tr = {}

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oT = Tokenise(old)
  nT = Tokenise(new)

  sm = difflib.SequenceMatcher(None, oT, nT)

  if sm.ratio() < 0.4: return None

  s = sm.get_matching_blocks()
  s.insert(0, difflib.Match(-1, -1, 1))

  findReplaces = {}

  for (cur, nex) in Pairwise(s):
    oldChunkLow = cur.a + cur.size
    oldChunkHi = nex.a 

    newChunkLow = cur.b + cur.size
    newChunkHi = nex.b

    if oldChunkLow == oldChunkHi: continue
    if newChunkLow == newChunkHi: continue

    oldSequence = oT[oldChunkLow : oldChunkHi]
    newSequence = nT[newChunkLow : newChunkHi]
    
    for oldToken, newToken in zip(oldSequence, newSequence):
      beforeOld, afterOld = re.search(neightbourRegex + re.escape(oldToken) + neightbourRegex, old).groups()
      beforeNew, afterNew = re.search(neightbourRegex + re.escape(newToken) + neightbourRegex, new).groups()

      if beforeNew != beforeOld: continue
      if afterNew != afterOld: continue

      if (oldToken in findReplaces and 
          (findReplaces[oldToken] is None or findReplaces[oldToken][0] != newToken)):
        findReplaces[oldToken] = None
        continue

      if oldToken in findReplaces:
        findReplaces[oldToken][1].append(beforeOld, afterOld, beforeNew, afterNew)

      findReplaces[oldToken] = newToken, [(beforeOld, afterOld, beforeNew, afterNew)]

  rt = ReplaceToken()

  for findToken in findReplaces.keys():
    replaceToken, neighbourList = findReplaces[findToken]

    if oT.count(findToken) != nT.count(replaceToken): continue
    if oT.count(replaceToken): continue
    if nT.count(findToken): continue

    for beforeOld, afterOld, beforeNew, afterNew in neighbourList:
      findText = beforeOld + findToken + afterOld
      replaceText = beforeNew + replaceToken + afterNew

      oldCount = old.count(findText)
      newCount = new.count(replaceText)

      if oldCount == newCount:
        rt.tr[findToken] = replaceToken

  if len(rt.tr.keys()) > 0: return rt
  return None


if __name__ == '__main__':
  Process("""
std::vector<sgC_PickInfo> sgC_SceneView::GetObjectPickHits(Tint32s X,
                                                           Tint32s Y)
          ""","""
std::vector<sgC_PickInformation> sgC_SceneView::GetObjectPickHits(
  Tint32s X, Tint32s Y)
  """)