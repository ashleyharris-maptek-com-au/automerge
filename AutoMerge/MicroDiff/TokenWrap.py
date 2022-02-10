
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
    self.prefix = ""
    self.suffix = ""
    self.filling = ""

    self.oldLow = ""
    self.oldHi = ""
    self.newLow = ""
    self.newHi = ""

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

  options = []

  for (a, b, c) in Triplewise(s):
    filling = " ".join(oT[b.a: b.a + b.size])
    if len(filling) < 3: continue
    if not re.match(r"\w+", filling): continue

    prefixIndex = a.a + a.size - 1

    if prefixIndex == -1: continue

    prefix = oT[prefixIndex]
    suffix = oT[c.a]

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

    tw = TokenWrap()
    tw.prefix = prefix
    tw.suffix = suffix
    tw.filling = filling
    tw.oldLow = abOld
    tw.oldHi = bcOld
    tw.newLow = abNew
    tw.newHi = bcNew

    if len(abOld) and len(bcOld) and len(abNew) and len(bcNew):
      # We're changing the bread of the token sandwhich
      # a = b(c,d);
      #     |   |
      # a = e(c,f);
      options.append(tw)

    elif len(abOld) and len(bcOld) and len(abOld) == 0and len(bcOld) == 0:
      #We're removing the bread from the token sandwich
      # a = b(c,d);
      #      / 
      # a = c;
      options.append(tw)

    elif len(abNew) and len(bcNew) and len(abOld) == 0 and len(bcOld) == 0:
      #We're adding bread to our token sandwhich
      # a =   b(c,d) ;
      #       
      # a = e(b(c,d));
      #     ||      |
      #     New tokens
      options.append(tw)

  # Now go thorugh all the options, pick the ones that make the most sense and
  # check they work, and return them
  raise NotImplemented()


if __name__ == '__main__':
  Process("auto item = MyClass(data);",
          "auto items = std::vector<MyClass>(3, data);")

