
"""

Represents a way to find a character (or character sequence) 
in a short section of text, this may be step
two of a multi step landmark.

"""

from collections import namedtuple
import sys, inspect
import math

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

class CharacterPrefix(namedtuple('CharacterPrefix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    prefixLength = 0

    while True:
      prefixLength += 1
      if begin - prefixLength <= 0: return None
      prefix = string[begin - prefixLength : begin]

      if string.count(prefix) > 1: continue

      return CharacterPrefix(prefix)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    matches = []
    for result in re.finditer(re.escape(self.impl),string):
      matches.append(result.span()[1])

    score = 1.0 / len(matches)

    for m in matches:
      bScores[m] += score







class CharacterSuffix(namedtuple('CharacterSuffix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    suffixLength = 0

    while True:
      suffixLength += 1
      if end + suffixLength == len(string): return None
      suffix = string[end : end + suffixLength]

      if string.count(suffix) > 1: continue

      return CharacterSuffix(suffix)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    matches = []
    for result in re.finditer(re.escape(self.impl),string):
      matches.append(result.span()[0])

    score = 1.0 / len(matches)

    for m in matches:
      eScores[m] += score











class TokenPrefix(namedtuple('TokenPrefix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    stringTokens = Tokenise(string)
    prefixTokens = Tokenise(string[0:begin])

    if len(prefixTokens) == 0: return None

    if stringTokens[len(prefixTokens) - 1] != prefixTokens[-1]:
      return None # We're in the middle of a token

    if stringTokens.count(prefixTokens[-1]) == 1:
      return TokenPrefix(prefixTokens[-1])

    raise NotImplementedError() # Build the longest sequence

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    tokens = Tokenise(string)

    if self.impl not in tokens:
      # partial match token implementation
      raise NotImplementedError()

    if tokens.count(self.impl) > 1: return None

    if self.impl == tokens[-1]:
      raise NotImplementedError()

    index = tokens.index(self.impl)

    regEx = r"\b" + re.escape(tokens[index]) + r"\b(.*)\b" + re.escape(tokens[index + 1])

    match = list(re.finditer(regEx,string))[0]

    b,e = match.regs[1]

    c = e - b + 1
    cc = 1.0 / c

    for ci in range(b,e + 1):
      bScores[ci] += cc









class TokenSuffix(namedtuple('TokenSuffix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    stringTokens = Tokenise(string)
    suffixTokens = Tokenise(string[end:])

    if len(suffixTokens) == 0: return None

    if stringTokens[0] != suffixTokens[0]:
      return None # We're in the middle of a token

    if stringTokens.count(suffixTokens[0]) == 1:
      return TokenPrefix(suffixTokens[0])

    raise NotImplementedError() # Build the longest sequence


  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    tokens = Tokenise(string)

    if self.impl not in tokens:
      # partial match token implementation
      raise NotImplementedError()

    if tokens.count(self.impl) > 1: return None

    if self.impl == tokens[0]:
      raise NotImplementedError()

    index = tokens.index(self.impl)

    regEx = r"\b" + re.escape(tokens[index - 1]) + r"\b(.*)\b" + re.escape(tokens[index])

    match = list(re.finditer(regEx, string, re.DOTALL ))[0]

    b,e = match.regs[1]

    c = e - b + 1
    cc = 1.0 / c

    for ci in range(b, e + 1):
      eScores[ci] += cc










class GrammarPartition(namedtuple('GrammarPartition',['before', 'mid', 'after'])):
  def ToGrammar(s :str):
    punc = re.findall(r"\W+",s.strip())
    punc = re.sub(r"\s+", "", "".join(punc))
    return punc


  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = GrammarPartition.ToGrammar(string[0:begin])
    mid = GrammarPartition.ToGrammar(string[begin:end])
    after = GrammarPartition.ToGrammar(string[end:])

    if before + after == "": return None

    return GrammarPartition(before,mid,after)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    strGrammarWithSpaces = re.sub(r"[\s\w]"," ")
    strGrammarWithoutSpaces = strGrammarWithSpaces.replace(" ", "")
    
    if strGrammarWithoutSpaces != self.before + self.mid + self.after:
      # Partial implementation needs to be done...
      raise NotImplementedError()

    sWs = ""
    sNs = ""
    stage = 0

    bookMarks = []

    for a in range(0, len(strGrammarWithSpaces)):
      if stage == 0 and sNs == self.before:
        bookMarks.append(a)
        stage = 1
      elif stage == 1 and sNs != self.before:
        bookMarks.append(a)
        stage = 2
      elif stage == 2 and sNs == self.before:
        bookMarks.append(a)
        stage = 3
      elif stage == 3 and sNs != self.before:
        bookMarks.append(a)
        break

      if not strGrammarWithSpaces[a].isspace():
        sNs += strGrammarWithSpaces[a]

      sWs += strGrammarWithSpaces[a]

    r = bookMarks[1] - bookMarks[0] + 1
    score = 1.0 / r
    for a in range(bookMarks[0], bookMarks[1]):
      bScores[a] += score

    r = bookMarks[3] - bookMarks[2] + 1
    score = 1.0 / r
    for a in range(bookMarks[3], bookMarks[2]):
      eScores[a] += score






class CharacterParition(namedtuple('CharacterParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(string[0:begin])
    mid = set(string[begin:end])
    after = set(string[end:])

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return CharacterParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    m = ""
    for c in string:
      if c in self.before: m += "b"
      elif c in self.mid: m += "m"
      elif c in self.after: m += "a"
      else: m += " "

    bMax = m.rfind("b")
    aMin = m.find("a")

    mMin = m.find("m")
    mMax = m.rfind("m")

    # No begin or end characters - just anchor to the end
    if bMax == -1: bMax = 0
    if aMin == -1: aMin = len(string)

    # No middle characters - makes things easier:
    if mMin == -1:

      if aMin < bMax:
        # We have overlap - ew.
        # BeginBeginEnBeginEndEndBeginBeginBegin
        #           ^^^^^^^^^^^^^ Any of these can be the boundary
        #

        scoreZeroLength = 1.0 / ( bMax - aMin + 1)

        scoreNonZeroLength = scoreZeroLength / 2
        if len(self.mid) == 0:
          # There was likely nothing in the middle - favour zero lengths.
          scoreNonZeroLength /= 4

        for i in range(aMin, bMax + 1):
          beMatrix[(i,i)] += scoreZeroLength

        for i in range(aMin, bMax):
          for j in range(i + 1, bMax + 1):
            beMatrix[(i,i)] += scoreNonZeroLength


      elif aMin >= bMax:
        # That's nice and sorted. "BeginBeginBegin   EndEndEnd"
        score = 1.0 / ( aMin - bMax + 1)

        if len(self.mid) == 0:
          # No middle wanted, or found
          for i in range(bMax, aMin + 1):
            beMatrix[(i,i)] += score

        else:
          # We wanted a middle, but didn't find it. Urgh
          score *= score
          for i in range(aMin, bMax + 1):
            for j in range(i, bMax + 1):
              beMatrix[(i,i)] += score

    else:
      raise NotImplementedError()





class CharacterPairParition(namedtuple('CharacterPairParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(Pairwise(string[0:begin]))
    mid = set(Pairwise(string[begin:end]))
    after = set(Pairwise(string[end:]))

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return CharacterPairParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    bS = []
    eS = []
    mS = []

    for pair in self.before:
      f = string.rfind(pair)
      if f != -1: bS.append(pair + 1)

    for pair in self.after:
      f = string.find(pair)
      if f != -1: eS.append(pair - 1)

    for pair in self.mid
      f = string.find(pair)
      if f != -1: mS.append(pair - 1)

    bS.sort()
    eS.sort()
    mS.sort()

    if not mS and not eS and not bS: return None

    if not bS: bS.append(0)
    if not eS: eS.append(len(string))

    score = 1.0

    if not mS:
      # No middle matches - that's easier

      if bS[-1] <= eS[0]:
        # Sorting is good
        b = bS[-1]
        e = eS[0]
      else:
        # Sorting is bad - some overlap between first begin and last end
        e = bS[-1]
        b = eS[0]

        score /= 4.0

    else:
      raise NotImplementedError()

    score = score / (e - b + 1)

    for i in range(b, e + 1):
      beMatrix[(i,i)] += score

    for i in range(b, e + 1):
      for j in range(i + 1, e + 1):
        beMatrix[(i,i)] += score




class TokenParition(namedtuple('TokenParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(Tokenise(string[0:begin]))
    mid = set(Tokenise(string[begin:end]))
    after = set(Tokenise(string[end:]))

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return TokenParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    bS = []
    eS = []
    mS = []

    for token in self.before:
      f = string.rfind(pair)
      if f != -1: bS.append(pair + 1)

    for token in self.after:
      f = string.find(pair)
      if f != -1: eS.append(pair - 1)

    for token in self.mid
      f = string.find(pair)
      if f != -1: mS.append(pair - 1)

    bS.sort()
    eS.sort()
    mS.sort()

    if not mS and not eS and not bS: return None

    if not bS: bS.append(0)
    if not eS: eS.append(len(string))

    score = 1.0

    if not mS:
      # No middle matches - that's easier

      if bS[-1] <= eS[0]:
        # Sorting is good
        b = bS[-1]
        e = eS[0]
      else:
        # Sorting is bad - some overlap between first begin and last end
        e = bS[-1]
        b = eS[0]

        score /= 4.0

    else:
      raise NotImplementedError()

    score = score / (e - b + 1)

    for i in range(b, e + 1):
      beMatrix[(i,i)] += score

    for i in range(b, e + 1):
      for j in range(i + 1, e + 1):
        beMatrix[(i,i)] += score










class TokenCount(namedtuple('TokenCount',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return TokenCount(
      len(Tokenise(string[0:begin])),
      len(Tokenise(string[begin:end])),
      len(Tokenise(string[end:])))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    l = list(re.finditer(r"\b\w+\b",string))

    expectedTokens = self.before + self.mid + self.after

    ratio =  float(len(l)) / float(expectedTokens)

    bOffset = ratio * self.before
    eOffset = ratio * (self.before + self.mid)

    span = abs(len(l) - expectedTokens) / 2
    if (span > bOffset or span > self.after): span /= 2

    if span < 1: span = 1

    firstBegin = math.floor(bOffset - span)
    lastBegin = math.ceil(bOffset + span)

    firstEnd = math.floor(eOffset - span)
    lastEnd = math.ceil(eOffset + span)

    for i in range(b, e + 1):
      for j in range(i + 1, e + 1):
        beMatrix[(i,i)] += score





class CharCount(namedtuple('CharCount',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return CharCount(
      len(string[0:begin].replace(r"\s+","")),
      len(string[begin:end].replace(r"\s+","")),
      len(string[end:].replace(r"\s+","")))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class GrammarScopeCounter(namedtuple('GrammarScopeCounter',['before', 'mid', 'after'])):
  def ScopeCount(s : str):
    return [
      s.count('(') - s.count(')'),
      s.count('[') - s.count(']'),
      s.count('{') - s.count('}'),
      s.count('<') - s.count('>')]

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = GrammarScopeCounter.ScopeCount(string[0:begin])
    mid = GrammarScopeCounter.ScopeCount(string[begin:end])
    after = GrammarScopeCounter.ScopeCount(string[end:])

    return GrammarScopeCounter(before, mid, after)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class DeltaTokens(namedtuple('DeltaTokens',['token', 'beforeCount', 'midCount', 'afterCount'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = Tokenise(string[0:begin])
    mid = Tokenise(string[begin:end])
    after = Tokenise(string[end:])

    inboth = set(before).intersection(set(after))

    l = []

    for token in inboth:
      l.append(
        DeltaTokens(token, before.count(token), mid.count(token), after.count(token)))
    
    return l

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class DeltaChars(namedtuple('DeltaChars',['char','left','mid','right'])):
  def CharMap(alphabet : str, s : str):
    g = {}
    for c in alphabet: 
      if not c.isspace():
        g[c] = 0
    for c in s: 
      if not c.isspace():
        g[c] += 1
    return g

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = string[0:begin]
    mid = string[begin:end]
    after = string[end:]

    b = DeltaChars.CharMap(string, before)
    m = DeltaChars.CharMap(string, mid)
    e = DeltaChars.CharMap(string, after)

    best = []

    for c in b.keys():
      best.append((sum([b[c], m[c], e[c]]),c,b[c], m[c], e[c]))

    best.sort(reverse=True)

    if len(best) > 4: best = best[0:4]

    results = []

    for s, c, b, m, e in best:
      results.append(DeltaChars(c, b, m, e))

    return results



  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class DeltaGrammar(namedtuple('DeltaGrammar',['before', 'mid', 'after'])):
  def ToGrammar(s :str):
    punc = re.findall(r"\W+",s.strip())
    punc = re.sub(r"\s+", "", "".join(punc))
    return [c for c in punc]

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(DeltaGrammar.ToGrammar(string[0:begin]))
    mid = set(DeltaGrammar.ToGrammar(string[begin:end]))
    after = set(DeltaGrammar.ToGrammar(string[end:]))

    return DeltaGrammar(before - (mid | after), mid - (before | after), after - (before | mid))


  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class SelectionString(namedtuple('SelectionString',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionString(string[begin:end])

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class SelectionTokens(namedtuple('SelectionTokens',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionTokens(Tokenise(string[begin:end]))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class SelectionBoundingChars(namedtuple('SelectionBoundingChars',['begin', 'end'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionBoundingChars(
      string[begin - 1 : begin + 1],
      string[end - 1 : end + 1])

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

class CharOffset(namedtuple('CharOffset',['selectors', 'region', 'charOffset'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    if not allowRecurse: return None
    res = []
    for d in [2, 4, 8, 16, 32, 64, 128]:
      if begin != end:
        sel = FindAllCharSelectors(string, begin - d, begin - d, False)
        if sel: res.append(CharOffset(sel,'begin', - d))

        sel = FindAllCharSelectors(string, begin + d, begin + d, False)
        if sel: res.append(CharOffset(sel,'begin', d))

        sel = FindAllCharSelectors(string, end - d, end - d, False)
        if sel: res.append(CharOffset(sel,'end', - d))

        sel = FindAllCharSelectors(string, end + d, end + d, False)
        if sel: res.append(CharOffset(sel,'end', d))

      sel = FindAllCharSelectors(string, begin - d, end - d, False)
      if sel: res.append(CharOffset(sel,'region', - d))

      sel = FindAllCharSelectors(string, begin + d, end + d, False)
      if sel: res.append(CharOffset(sel,'region', d))
    return res

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass


class TokenOffset(namedtuple('TokenOffset',['selectors', 'region', 'charOffset'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    if not allowRecurse: return None

    tokens = list(re.finditer(r"\b\w+\b",string))

    beginIndex = 0
    while tokens[beginIndex].span()[1] < begin: beginIndex += 1
    beginIndex -= 1

    endIndex = beginIndex
    while tokens[endIndex].span()[0] < end: endIndex += 1

    res = []
    for d in [1, 2, 4, 8, 16]:
      nb = beginIndex - d
      if nb >= 0:
        sel = FindAllCharSelectors(string, tokens[nb].span()[0], tokens[nb].span()[1], False)
        if sel: res.append(TokenOffset(sel,'begin', -d))
      ne = endIndex + d
      if ne < len(tokens):
        sel = FindAllCharSelectors(string, tokens[nb].span()[0], tokens[nb].span()[1], False)
        if sel: res.append(TokenOffset(sel,'end', -d))
    return res

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, bScores : list, eScores : list, beMatrix : dict):
    pass

def FindAllCharSelectors(
  string : str, begin : int, end : int, allowRecurse = True) -> list:

  if begin < 0 or begin >= len(string): return None
  if end < 0 or end >= len(string): return None

  clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

  choices = []

  for cls in clsmembers:
    result = cls[1].Process(string, begin, end, allowRecurse)
    if result is None: continue
    if isinstance(result, list): choices.extend(result)
    else: choices.append(result)

  return choices

def Apply(string : str, selectors : list):
  bScore = [0.0] * len(string)
  eScore = [0.0] * len(string)
  beMatrix = Dict0()
  
  for sel in selectors:
    sel.Apply(string, bScore, eScore, beMatrix)

  for i in range(len(string)):
    if bScore[i] > 0:
      for j in range(len(string)):
        if eScore[j] == 0.0: continue
        key = (i, j)
        if key in beMatrix: beMatrix[key] += bScore[i]
        else: beMatrix[key] = bScore[i]

    if eScore[i] > 0:
      for j in range(len(string)):
        if bScore[j] == 0.0: continue
        key = (j, i)
        if key in beMatrix: beMatrix[key] += eScore[i]
        else: beMatrix[key] = eScore[i]

  
  maxKey = max(beMatrix, key=beMatrix.get)

  return maxKey

def RunUnitTest(prefix : str, mid : str, suffix : str):
  string = prefix + mid + suffix

  selectors = FindAllCharSelectors(string, len(prefix), len(prefix) + len(mid))

  Apply(string,selectors)

  i = 0

if __name__ == '__main__':
  RunUnitTest("if (Bitrate == numN::","","Upper<Tint32u>())")