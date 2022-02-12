"""

Represents a way to find a line, this may be step
one of a multi step landmark.

"""

from collections import namedtuple

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

import sys, inspect

class LineLengthExtremes(namedtuple('LineLengthExtremes', ['operation'])):
  def Process(Lines : list, Index : int, allowRecurse = True):

    if Lines[Index].strip() == "": return LineLengthExtremes('blank')

    sortedLines = sorted(filter(lambda x: x.strip() != "", Lines),key=len,reverse=True)

    longestLineLength = len(sortedLines[0])

    if len(Lines[Index]) == longestLineLength:
      if longestLineLength == len(sortedLines[1]):
        return LineLengthExtremes('equalLongest') 
      return LineLengthExtremes('longest')

    shortestLineLength = len(sortedLines[-1])
    if len(Lines[Index]) == shortestLineLength:
      if shortestLineLength == len(sortedLines[-2]):
        return LineLengthExtremes('equalShortest') 
      return LineLengthExtremes('shortest')

    return None

  def Summary(self):
    return self.operation

  def Apply(self, Lines : list, Scores : list):
    ls = [f.strip() for f in Lines]

    if self.operation == 'blank':
      blankLines = ls.count("")
      score = 1.0 / blankLines
      for i in range(len(Lines)):
        if ls[i] == "": Scores[i] += score
    else:
      lss = list(filter(lambda x: x > 0, [len(x) for x in ls]))
      lss.sort()

      if self.operation == 'shortest' or self.operation == 'equalShortest':
        tll = lss[0]
      elif self.operation == 'longest' or self.operation == 'equalLongest':
        tll = lss[-1]

      count = lss.count(tll)

      score = 1.0 / count

      if 'equal' in self.operation and count > 1: score *= 2

      for i in range(len(Lines)):
        if len(ls[i]) == tll: Scores[i] += score



class LineTokenHistgram(namedtuple('LineTokenHistgram', ['operation', 'tokens'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    otherTokens = set()
    targetTokens = set(Tokenise(Lines[Index]))

    for l in range(len(Lines)):
      if l == Index: continue
      otherTokens.update(Tokenise(Lines[l]))

    uniqueToTargetLine = targetTokens - otherTokens

    if uniqueToTargetLine:
      return LineTokenHistgram('onlyLineWith', uniqueToTargetLine)

    notOnTargetLine = otherTokens - targetTokens

    matches = []
    for l in Lines:
      anyToken = False
      for t in notOnTargetLine:
        if t in l:
          anyToken = True
          break
      if anyToken: continue
      matches.append(l)

    if len(matches) == 1 and matches[0] == Lines[Index]:
      return LineTokenHistgram('onlyLineWithout', notOnTargetLine)

    return

  def Summary(self):
    if self.operation == 'onlyLineWith':
      return "only line with " + NiceTokenList(self.tokens)
    if self.operation == 'onlyLineWithout':
      return "only line without " + NiceTokenList(self.tokens)

  def Apply(self, Lines : list, Scores : list):
    for i in range(len(Lines)):
      tokens = set(Tokenise(Lines[i]))

      if self.operation == 'onlyLineWith':
        intersect = tokens.intersection(self.tokens)
        score = float(len(intersect)) / len(self.tokens)
        Scores[i] += score * score
      elif self.operation == 'onlyLineWithout':
        intersect = tokens.intersection(self.tokens)
        score = 1.0 - float(len(intersect)) / len(self.tokens)
        Scores[i] += score * score






class LineCharHistgram(namedtuple('LineCharHistgram', ['operation', 'tokens'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    otherTokens = set()
    targetTokens = set(Lines[Index])

    for l in range(len(Lines)):
      if l == Index: continue
      otherTokens.update(Lines[l])

    uniqueToTargetLine = targetTokens - otherTokens

    if uniqueToTargetLine:
      return LineTokenHistgram('onlyLineWith', uniqueToTargetLine)

    notOnTargetLine = otherTokens - targetTokens

    matches = []
    for l in Lines:
      anyToken = False
      for t in notOnTargetLine:
        if t in l:
          anyToken = True
          break
      if anyToken: continue
      matches.append(l)

    if len(matches) == 1 and matches[0] == Lines[Index]:
      return LineTokenHistgram('onlyLineWithout', notOnTargetLine)

  def Summary(self):
    if self.operation == 'onlyLineWith':
      return "only line with " + NiceTokenList(self.tokens)
    if self.operation == 'onlyLineWithout':
      return "only line without " + NiceTokenList(self.tokens)

  def Apply(self, Lines : list, Scores : list):
    for i in range(len(Lines)):
      tokens = set(Lines[i])

      if self.operation == 'onlyLineWith':
        intersect = tokens.intersection(self.tokens)
        score = float(len(intersect)) / len(self.tokens)
        Scores[i] += score * score
      elif self.operation == 'onlyLineWithout':
        intersect = tokens.intersection(self.tokens)
        score = 1.0 - float(len(intersect)) / len(self.tokens)
        Scores[i] += score * score

class LineDumbContents(namedtuple('LineDumbContents', ['contents'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    if Lines[Index].strip() == "": return None

    if Lines.count(Lines[Index]) > 1: return None

    return LineDumbContents(Lines[Index])

  def Summary(self):
    return "most similar to: " + self.contents

  def Apply(self, Lines : list, Scores : list):
    ratios = [Ratio(x, self.contents) for x in Lines]

    bestRatio = max(ratios)

    if bestRatio < 0.5: return

    ratios = [x / bestRatio for x in ratios]
    ratios = [x * x for x in ratios]

    for i in range(len(Lines)):
      if ratios[i] < 0.1: continue
      Scores[i] += ratios[i]



class LineDumbNeighbours(namedtuple('LineDumbNeighbours', ['above', 'below'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    if allowRecurse == False: return None

    if Index == 0:
      return LineDumbNeighbours(None, Lines[1])

    if Index == len(Lines) - 1:
      return LineDumbNeighbours(Lines[Index - 1], None)
    
    return LineDumbNeighbours(Lines[Index - 1], Lines[Index + 1])

  def Summary(self):
    return (
      "between " +
      (self.above if self.above else "(Start)") +
      " and " +
      (self.below if self.below else "(End)"))


  def Apply(self, Lines : list, Scores : list):
    if self.above is not None:
      aboveLineRatios = [Ratio(x, self.above) for x in Lines]
    else:
      aboveLineRatios = [0] * len(Lines)

    if self.below is not None:
      belowLineRatios = [Ratio(x, self.below) for x in Lines]
    else:
      belowLineRatios = [0] * len(Lines)

    totalRatios = [0] * len(Lines)
    for i in range(0,len(Lines)):
      if i > 0: totalRatios[i] += aboveLineRatios[i-1]
      if i > 1: totalRatios[i] += aboveLineRatios[i-2] * 0.25
      if i < len(Lines) - 1: totalRatios[i] += belowLineRatios[i+1]
      if i < len(Lines) - 2: totalRatios[i] += belowLineRatios[i+2] * 0.25

    if self.above is None: 
      totalRatios[0] += 1.0
      totalRatios[1] += 0.25

    if self.below is None: 
      totalRatios[-1] += 1.0
      totalRatios[-2] += 0.25
    
    for i in range(0,len(Lines)):
      Scores[i] += totalRatios[i]


class LineDeltaFromNeighbour(namedtuple('LineDeltaFromNeighbour', ['selector', 'delta'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    
    if not allowRecurse: return None

    options = []

    for l in range(max(0, Index - 2), min(len(Lines)-1, Index + 3)):
      if l == Index: continue

      lineSelectors = FindAllLineSelectors(Lines, l, False)

      if len(lineSelectors) == 0: continue

      for ls in lineSelectors:
        options.append(LineDeltaFromNeighbour(ls, l - Index))

    return options

  def Summary(self):
    if self.delta == -2: return "2 lines after " + self.selector.Summary()
    if self.delta == -1: return "line after " + self.selector.Summary()
    if self.delta == 2: return "2 lines before " + self.selector.Summary()
    if self.delta == 1: return "line before " + self.selector.Summary()

  def Apply(self, Lines : list, Scores : list):
    nScores = [0] * len(Lines)

    self.selector.Apply(Lines, nScores)

    for i in range(0,len(Lines)):
      deltaLine = i + self.delta

      if deltaLine < 0: continue
      if deltaLine >= len(Lines): continue

      Scores[i] += nScores[deltaLine] * 0.2

    

class LineTokenIndex(namedtuple('LineTokenIndex',['token', 'operation'])):
  def Process(Lines : list, Index : int, allowRecurse = True):
    
    tokensBefore = {}
    tokensAfter = {}
    tokenMaps = []

    for l in range(Index):
      for token in Tokenise(Lines[l]):
        if token in tokensBefore: tokensBefore[token] += 1
        else: tokensBefore[token] = 1

    for l in range(Index + 1, len(Lines)):
      for token in Tokenise(Lines[l]):
        if token in tokensAfter: tokensAfter[token] += 1
        else: tokensAfter[token] = 1

    for token in set(Tokenise(Lines[Index])):
      if token not in tokensAfter and token not in tokensBefore:
        tokenMaps.append(LineTokenIndex(token, 'only'))
      elif token not in tokensAfter:
        tokenMaps.append(LineTokenIndex(token, 'last'))
      elif token not in tokensBefore:
        tokenMaps.append(LineTokenIndex(token, 'first'))
      elif tokensBefore[token] == 1:
        tokenMaps.append(LineTokenIndex(token, 'second'))
      elif tokensAfter[token] == 1:
        tokenMaps.append(LineTokenIndex(token, 'secondToLast'))

    return tokenMaps

  def Summary(self):
    return self.operation + " " + self.token

  def Apply(self, Lines : list, Scores : list):
    tokenLineOccurance = []

    for l in range(len(Lines)):
      if self.token in Tokenise(Lines[l]):
        tokenLineOccurance.append(l)

    if len(tokenLineOccurance) == 0: return

    if len(tokenLineOccurance) == 1:
      if self.operation == 'second' or self.operation == 'secondToLast':
        # There were > 3, we were in the middle and now there's one... smells fishy
        Scores[tokenLineOccurance[0]] += 0.25
      elif self.operation == 'only':
        # There was one and now there's one: woot.
        Scores[tokenLineOccurance[0]] += 1.0
      else:
        # There was >2 and now there's only one. Not great but a useful hint.
        Scores[tokenLineOccurance[0]] += 0.5

    elif len(tokenLineOccurance) == 2:
      if self.operation == 'first':
        Scores[tokenLineOccurance[0]] += 1.0

      elif self.operation == 'last':
        Scores[tokenLineOccurance[1]] += 1.0

      elif self.operation == 'only':
        Scores[tokenLineOccurance[0]] += 0.25
        Scores[tokenLineOccurance[1]] += 0.25

      else:
        Scores[tokenLineOccurance[0]] += 0.15
        Scores[tokenLineOccurance[1]] += 0.15

    else:
      if self.operation == 'only':
        pass
      elif self.operation == 'first':
        Scores[tokenLineOccurance[0]] += 0.95
        Scores[tokenLineOccurance[1]] += 0.05
      elif self.operation == 'last':
        Scores[tokenLineOccurance[-1]] += 0.95
        Scores[tokenLineOccurance[-2]] += 0.05
      elif self.operation == 'second':
        Scores[tokenLineOccurance[0]] += 0.05
        Scores[tokenLineOccurance[1]] += 0.90
        Scores[tokenLineOccurance[2]] += 0.05
      elif self.operation == 'secondToLast':
        Scores[tokenLineOccurance[-1]] += 0.05
        Scores[tokenLineOccurance[-2]] += 0.90
        Scores[tokenLineOccurance[-3]] += 0.05


class TokenNGrams(namedtuple('TokenNGrams',['tokenSequences'])):
  def Process(Lines : list, Index : int, allowRecurse = True):

    nGramsInLine = set()

    tokenString = ""

    for l in range(len(Lines)):
      if l == Index: continue

      tokens = Tokenise(Lines[l])
      tokenString += " ".join(tokens)
      tokenString += " "
      
    tokens = Tokenise(Lines[Index])

    for a in range(len(tokens)):
      for b in range(a + 2, len(tokens) + 1):
        nGram = " ".join(tokens[a:b])

        if nGram in tokenString: continue

        nGramsInLine.add(nGram)

    if nGramsInLine:
      return TokenNGrams(nGramsInLine)

  def Summary(self):
    return "only line with N-Grams: " + NiceTokenList(self.tokenSequences)

  def Apply(self, Lines : list, Scores : list):
    lCount = [0] * len(Lines)

    for l in range(len(Lines)):
      tokens = " ".join(Tokenise(Lines[l]))

      for nGram in self.tokenSequences:
        if nGram in tokens:
          lCount[l] += 1

    maxMatch = max(lCount)

    if maxMatch == 0: return

    lCount = [float(x) / maxMatch for x in lCount]
    lCount = [x * x for x in lCount]

    for l in range(len(Lines)):
      Scores[l] += lCount[l]

class IsolatedSignificantTokens(namedtuple('IsolatedSignificantTokens',['tokenDeltaList'])):
  def Process(Lines : list, Index : int, allowRecurse = True):

    if allowRecurse == False: return None

    info = []

    for l in range(max(0, Index - 5), min(len(Lines)-1, Index + 6)):
      ls = Lines[l].strip()
      if ls == "": continue
      lc = ls[-1]
      fc = ls[0]

      if (lc == ":" or lc == "{" or lc == "(" or lc == "[" or lc == "<"):
        info.append((Index - l, 'endswith', lc))
      elif (fc == "}" or fc == ")" or fc == "]" or fc == ">"):
        info.append((Index - l, 'startswith', fc))

    if len(info) == 0: return None

    info.sort(key=lambda x: abs(x[0]))

    info = info[0:2]

    info.sort(key=lambda x: x[1], reverse=True)

    return IsolatedSignificantTokens(info)

  def Summary(self):
    s = ""
    for delta, lineStyle, symbol in self.tokenDeltaList:
      if abs(delta) == 1: s += "1 line "
      else: s += str(abs(delta)) + " lines "

      if delta > 0: s += "after "
      else: s += "before "

      s += symbol

      if lineStyle == 'endswith': s += " at end of line"
      else: s += " at start of line"
      s += ". "

    return s.strip()

  def Apply(self, Lines : list, Scores : list):
    def findLine(deltaList):
      results = []
      for q in range(len(Lines)):
        if deltaList[1] == 'startswith' and Lines[q].lstrip().startswith(deltaList[2]):
          results.append(q)
        if deltaList[1] == 'endswith' and Lines[q].strip().endswith(deltaList[2]):
          results.append(q)
      return results

    if len(self.tokenDeltaList) == 2 and self.tokenDeltaList[0][0] > 0 and self.tokenDeltaList[1][0] < 0:
      self.tokenDeltaList.reverse()


    if len(self.tokenDeltaList) == 1:
      results = findLine(self.tokenDeltaList[0])

      for lineNo in results:
        steps = abs(self.tokenDeltaList[0][0])

        Scores[lineNo] += 1.0
        for delta in range(1, steps):
          score = 1.0 - float(delta) / float(steps)
          Scores[lineNo + delta] += score
          Scores[lineNo - delta] += score
      

    elif self.tokenDeltaList[0][0] < 0 and self.tokenDeltaList[1][0] > 0:
      begins = findLine(self.tokenDeltaList[1])
      ends = findLine(self.tokenDeltaList[0])

      countOfRuns = 0

      for begin in begins:
        for end in ends:
          if begin < end: countOfRuns += 1

      previousSpan = self.tokenDeltaList[1][0] - self.tokenDeltaList[0][0]
      ratioToLine = float(self.tokenDeltaList[1][0]) / previousSpan

      runScaling = 1.0 / countOfRuns

      for begin in begins:
        for end in ends:
          if begin >= end: continue

          newSpan = end - begin

          targetLine = ratioToLine * newSpan + begin

          for line in range(begin + 1, end):
            delta = abs(line - targetLine)
            delta /= max(newSpan,previousSpan)

            Scores[line] += (1.0 - delta) * runScaling



    else:
      raise NotYetImplementedError()


    pass

class LineGrammar(namedtuple('LineGrammar',['tokenSequence'])):
  def ToGrammar(s :str):
    punc = re.findall(r"\W+",s.strip())
    punc = re.sub(r"\s+", "", "".join(punc))
    return punc

  def Process(Lines : list, Index : int, allowRecurse = True):
    punc = LineGrammar.ToGrammar(Lines[Index].strip())
    if punc == "": return None
    return LineGrammar(punc)

  def Summary(self):
    return "grammar sequence: " + self.tokenSequence

  def Apply(self, Lines : list, Scores : list):
    ratios = [Ratio(LineGrammar.ToGrammar(x), self.tokenSequence) for x in Lines]

    bestRatio = max(ratios)

    if bestRatio < 0.5: return

    ratios = [x / bestRatio for x in ratios]
    ratios = [x * x for x in ratios]

    for i in range(len(Lines)):
      if ratios[i] < 0.5: continue
      Scores[i] += ratios[i]


def FindAllLineSelectors(
  Lines : list, ValidIndex : int, allowRecurse = True) -> list:

  clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

  choices = []

  for cls in clsmembers:
    if "Process" not in cls[1].__dict__: continue
    result = cls[1].Process(Lines, ValidIndex, allowRecurse)
    if result is None: continue
    if isinstance(result, list): choices.extend(result)
    else: choices.append(result)

  return choices

def ApplyLineSelectorsToContent(LineSelectors : list, Lines : list) -> int:
  scores = [0.0] * len(Lines)

  for ls in LineSelectors:
    ls.Apply(Lines, scores)

  maxScore = 0.0
  maxIndex = None
  for i in range(len(Lines)):
    if scores[i] > maxScore:
      maxScore = scores[i]
      maxIndex = i

  return maxIndex, scores

def DebugPrintLineAndScore(Lines : list, Scores : list):
  maxScore = max(Scores)

  for r in range(len(Lines)):
    if Scores[r] == maxScore:
      print(">>>>>>>>>>",end="")
    else:
      tokens = int(Scores[r] / maxScore * 10)
      print("*" * tokens, end="")
      print(" " * (10 - tokens), end="")
    print(str(r).rjust(3), end=" ")
    print(Lines[r])


def RunUnitTest(text : str, lineNo : int, 
                expectedSelectors : str = None, 
                applyTo : str = None, 
                exectedIndex : int  = None):
  lines = text.strip("\n").splitlines()

  for r in range(len(lines)):
    if lineNo == r:
      print(str(r) + ":!!>\t" + lines[r])
    else:
      print(str(r) + ":\t" + lines[r])

  options = FindAllLineSelectors(lines, lineNo)

  print("----------------------------------")

  summary = []
  for option in options:
    summary.append(option.Summary().capitalize())

  summary.sort()

  summar = "\n".join(summary)

  print(summar)

  print("----------------------------------")

  sanityCheckResultIndex, scores1 = ApplyLineSelectorsToContent(options, lines)
  DebugPrintLineAndScore(lines, scores1)
  assert(lineNo == sanityCheckResultIndex)

  print("----------------------------------")

  if expectedSelectors is not None:
    assert(expectedSelectors.strip() == summar.strip())

  if applyTo is not None:
    newLines = applyTo.strip().splitlines()
    resultIndex, scores = ApplyLineSelectorsToContent(options, newLines)

    DebugPrintLineAndScore(newLines, scores)

    assert(resultIndex == exectedIndex)

    print("----------------------------------")




if __name__ == '__main__':
  test1 = RunUnitTest("""
// This is part 1:
a = 4 + 7;
    
// This is part 2 (not very interesting):
b = 22 * 22 - 22;
    
// This is part 3 (oooh pi):
c = pi * 4;
    """, 4, 
    expectedSelectors=  """
1 line after : at end of line. 2 lines before : at end of line.
2 lines after blank
2 lines before first pi
2 lines before grammar sequence: //():
2 lines before last is
2 lines before last part
2 lines before last this
2 lines before most similar to: // this is part 3 (oooh pi):
2 lines before only 3
2 lines before only line with 3
2 lines before only line with 3 and oooh
2 lines before only line with n-grams: 3 oooh, 3 oooh pi, this is part 3, this is part 3 oooh, this is part 3 oooh pi, is part 3, is part 3 oooh, is part 3 oooh pi, oooh pi, part 3, part 3 oooh and part 3 oooh pi
2 lines before only oooh
Between // this is part 2 (not very interesting): and     
Grammar sequence: =*-;
Line after grammar sequence: //():
Line after longest
Line after most similar to: // this is part 2 (not very interesting):
Line after only 2
Line after only interesting
Line after only line with 2, interesting, not and very
Line after only line with e, g, n, v and y
Line after only line with n-grams: 2 not, 2 not very, 2 not very interesting, this is part 2, this is part 2 not, this is part 2 not very, this is part 2 not very interesting, is part 2, is part 2 not, is part 2 not very, is part 2 not very interesting, not very, not very interesting, part 2, part 2 not, part 2 not very, part 2 not very interesting and very interesting
Line after only not
Line after only very
Line after second is
Line after second part
Line after second this
Line before blank
Most similar to: b = 22 * 22 - 22;
Only 22
Only b
Only line with - and b
Only line with 22 and b
Only line with n-grams: 22 22, 22 22 22, b 22, b 22 22 and b 22 22 22
""")

  test2 = RunUnitTest("""
      CULL_BACK,
      CULL_FRONT_AND_BACK
    };

    // What sort of texture will be specified
    enum Texture_Mode
    {
      TEXTURE_1D = 1,
      TEXTURE_2D = 2,
      TEXTURE_3D = 3
      //  TEXTURE_4D ?
    };

    // How textures should be displayed
    enum TextureDisplayMode
    {
      TEXTURE_OFF,
      TEXTURE_MODULATE,
""",8, 
    applyTo= """
    // What sort of texture will be specified
    enum class E_TextureMode
    {
      Texture1D = 1, 
      Texture2D = 2, // Includes 1D array and OpenGL 'rect' images.
      Texture3D = 3, // Includes 2D array and cubemaps
    };

    // Texture4D doesn't exist on modern GPUs
    """,
    exectedIndex=4)


