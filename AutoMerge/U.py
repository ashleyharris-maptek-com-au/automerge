import difflib, re

def Tokenise(s : str) -> list:
  return re.findall(r"\b\w+\b",s)

def TokenAndGrammar(s : str) -> list:
  tokens = list(re.finditer(r"\b\w+\b",s))

  allTok = [tokens[0].group()]

  for cur, nex in Pairwise(tokens):
    textBetween = s[cur.span()[1]: nex.span()[0]]

    operators = ToTypicalTokenList(textBetween)

    allTok.extend(operators)
    allTok.append(nex.group())

  allTok.extend(ToTypicalTokenList(s[tokens[-1].span()[1]:]))

  return allTok

def ToTypicalTokenList(operator : str):
  tokens = []
  while(len(operator)):
    if (operator.startswith("++") or operator.startswith("--") or
        operator.startswith("+=") or operator.startswith("-=") or
        operator.startswith("*=") or operator.startswith("/=") or
        operator.startswith("%=") or operator.startswith("==") or
        operator.startswith("!=") or operator.startswith(">=") or
        operator.startswith("/*") or operator.startswith("*/") or
        operator.startswith("<=") or operator.startswith("&&") or
        operator.startswith("||") or operator.startswith("<<") or
        operator.startswith(">>") or operator.startswith("->") or
        operator.startswith("//") or operator.startswith("::")):

      tokens.append(operator[0:2])
      operator = operator[2:]
      continue

    if operator[0] in " \n\t":
      operator = operator[1:]
      continue

    tokens.append(operator[0:1])
    operator = operator[1:]
  return tokens


def NiceTokenList(tokenList : list) -> str:
  tokens = list(tokenList)
  if len(tokens) == 0: return "None"
  if len(tokens) == 1: return tokens[0]

  tokens.sort()

  s = ""
  for i in range(len(tokens) - 1):
    s += tokens[i]
    s += ", "

  s = s[:-2]
  s += " and "
  s += tokens[-1]
  return s

def Ratio(a : str, b : str):
  return difflib.SequenceMatcher(a=a, b=b).ratio()

def RatioNoSpace(a : str, b : str):
  return difflib.SequenceMatcher(lambda x: x in " \t\n", a=a, b=b).ratio()

def RatioToken(a : str, b : str):
  return difflib.SequenceMatcher(a=Tokenise(a), b=Tokenise(b)).ratio()

def Pairwise(iterable):
  it = iter(iterable)
  a = next(it, None)

  for b in it:
      yield (a, b)
      a = b

def Triplewise(iterable):
  it = iter(iterable)
  a = next(it, None)
  b = next(it, None)

  for c in it:
      yield (a, b, c)
      a = b
      b = c

class Dict0(dict):
  def __missing__(self, key):
    return 0

def Clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def StripEqualOrContained(a : str, b : str):
  a = a.strip()
  b = b.strip()
  if a == b : return True
  
  if a and a in b: return True
  if b and b in a: return True

  return False
  
def NextIncrementingSequence(sequence : list):

  runStart = 0

  for q in range(1, len(sequence)):
    if sequence[q] == sequence[q - 1] + 1: continue
    else:
      return sequence[runStart], sequence[q - 1]

  if len(sequence) > 0: return sequence[0], sequence[-1]

  return None, None

def LineToLineMap(oldLines : list, newLines : list):
  """Returns a list of pairs mapping lines in old to their best matching lines in new"""

  oldLinesSet = set(oldLines)
  newLinesSet = set(newLines)

  exactMatches = list(oldLinesSet & newLinesSet)

  freeLinesIn1 = list(oldLinesSet - newLinesSet)
  freeLinesIn2 = list(newLinesSet - oldLinesSet)

  allScores = []

  for fl1 in freeLinesIn1:
    for fl2 in freeLinesIn2:
      allScores.append((Ratio(fl1, fl2), fl1, fl2))

  allScores.sort(reverse = True)

  lineToTextSource = {}
  l1sUsed = set()
  l2sUsed = set()

  for score, l1Text, l2Text in allScores:
    if score < 0.6: continue
    if l1Text in l1sUsed: continue
    if l2Text in l2sUsed: continue

    lineToTextSource[l2Text] = l1Text

    l1sUsed.add(l1Text)
    l2sUsed.add(l2Text)

  lineToLineMap = []

  for ln in range(len(newLines)):
    lnText = newLines[ln]

    if lnText in exactMatches:
      loText = lnText
      if oldLines.count(loText) != 1: continue
    elif lnText in lineToTextSource:
      loText = lineToTextSource[lnText]
      if oldLines.count(loText) != 1: continue
    else:
      continue

    sourceIndex = oldLines.index(loText)

    lineToLineMap.append((sourceIndex, ln))

  lineToLineMap.sort()

  return lineToLineMap

def LineToLineMapAndHalwayMap(oldLines : list, newLines : list):
  """Returns a lineToLineMap, and a halfway map - the old lines rearranged into their best guess
  new position, new lines inserted, deleted lines removed, but the old lines not changed yet."""

  lineToLineMap = LineToLineMap(oldLines, newLines)

  halfWayLines = newLines[:]

  for o,n in lineToLineMap:
    halfWayLines[n] = oldLines[o]

  return lineToLineMap, halfWayLines