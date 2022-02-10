
"""
=# 

Represents a token, or token sequence, wrapped by other token
sequnces.

=Old
const auto activeSetting = "active";
if (preferenceValue == activeSetting)
{
=New
const auto activeSetting = "active";
if (translate(preferenceValue) == activeSetting)
{
=Expect
Suround "preferenceValue" with:
"translate", "(",
")"
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

class TokenWrap:
  def __init__(self) -> None:
    self.tr = {}

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oT = TokenAndGrammar(old)
  nT = TokenAndGrammar(new)

  sm = difflib.SequenceMatcher(None, oT, nT)

  if sm.ratio() < 0.4: return None

  s = sm.get_matching_blocks()
  s.insert(0, difflib.Match(-1, -1, 1))

  for (a, b, c) in Triplewise(s):
    if not re.fullmatch(r"\w+", oT[b.a]): continue

    abOldLow = a.a + a.size
    abOldHi = b.a

    abOld = " ".join(oT[abOldLow : abOldHi])

    bcOldLow = b.a + b.size
    bcOldHi = c.a

    bcOld = " ".join(oT[bcOldLow : bcOldHi])

    abNewLow = a.b + a.size
    abNewHi = b.b

    abNew = " ".join(nT[abNewLow : abNewHi])

    bcNewLow = b.b + b.size
    bcNewHi = c.b

    bcNew = " ".join(nT[bcNewLow : bcNewHi])

    if len(abOld) and len(bcOld) and len(abNew) and len(bcNew):
      # We're changing the bread of the token sandwhich
      # a = b(c,d);
      #     |   |
      # a = e(c,f);
      qwe = 0

    elif len(abOld) and len(bcOld) and len(abOld) == 0and len(bcOld) == 0:
      #We're removing the bread from the token sandwich
      # a = b(c,d);
      #      / 
      # a = c;
      qwe = 0
    elif len(abNew) and len(bcNew) and len(abOld) == 0 and len(bcOld) == 0:
      #We're adding bread to our token sandwhich
      # a = b(c,d);
      #       
      # a = e(b(c,d));
      #     ||      ||
      #     New tokens
      qwe = 0


    qwe = 0


if __name__ == '__main__':
  Process("auto item = MyClass(data);",
          "auto items = std::vector<MyClass>(3, data);")

