import difflib

def ratio(a : str, b : str):
  return difflib.SequenceMatcher(a=a, b=b).ratio()

def pairwise(iterable):
  it = iter(iterable)
  a = next(it, None)

  for b in it:
      yield (a, b)
      a = b

def fuzzyLineFind(small : str, big : str):
  """Looks for a single line (small) roughly in big."""
  
  assert(small.count("\n") == 0)

  bigLines = big.splitlines()

  maxRatio = 0
  bestLine = ""

  for line in bigLines:
    r = ratio(a=line, b=small)

    if r > maxRatio:
      maxRatio = r
      bestLine = line

  return (bestLine, maxRatio)

def approximateCommonPrefix(a : str, b : str):
  while True:
    if len(a) < 10 or len(b) < 10: break

    d00 = ratio(a,b)

    aDrop1 = a[:-1]
    aDrop8 = a[:-8]
    bDrop1 = b[:-1]
    bDrop8 = b[:-8]

    d01 = ratio(a,bDrop1)
    d08 = ratio(a,bDrop8)
    d11 = ratio(aDrop1,bDrop1)
    d18 = ratio(aDrop1,bDrop8)
    d81 = ratio(aDrop8,bDrop1)
    d88 = ratio(aDrop8,bDrop8)
    d10 = ratio(aDrop1,b)
    d80 = ratio(aDrop8,b)

    winner = max(d00, d01, d08, d11, d18, d81, d88, d10, d80)

    if winner == d00: break

    if winner == d01 or winner == d11 or winner == d81:
      b = bDrop1
    elif winner == d08 or winner == d18 or winner == d88:
      b = bDrop8

    if winner == d10 or winner == d11 or winner == d18:
      a = aDrop1
    elif winner == d80 or winner == d81 or winner == d88:
      a = aDrop8

  while True:
    if len(a) == 0: return None
    if len(b) == 0: return None

    d00 = ratio(a,b)

    aDrop1 = a[:-1]
    bDrop1 = b[:-1]

    d01 = ratio(a,bDrop1)
    d11 = ratio(aDrop1,bDrop1)
    d10 = ratio(aDrop1,b)

    winner = max(d00, d01, d11, d10)

    if winner == d00: return (a, b)

    if winner == d01 or winner == d11:
      b = bDrop1

    if winner == d10 or winner == d11:
      a = aDrop1

def approximateCommonPrefixByLine(a : str, b : str):
  while True:
    if a.count("\n") == 0: return None
    if b.count("\n") == 0: return None

    d00 = ratio(a,b)

    aDrop1 = a.rsplit("\n", 1)[0]
    bDrop1 = b.rsplit("\n", 1)[0]

    d01 = ratio(a,bDrop1)
    d11 = ratio(aDrop1,bDrop1)
    d10 = ratio(aDrop1,b)

    winner = max(d00, d01, d11, d10)

    if winner == d00: return (a, b)

    if winner == d01 or winner == d11:
      b = bDrop1

    if winner == d10 or winner == d11:
      a = aDrop1



def approximateSubStringByLine(needle : str, haystack : str):

  if needle in haystack: return (needle, 1.0)

  hs = haystack.splitlines()
  a = 0
  b = len(hs)

  linesInNeedle = needle.count("\n")

  if b > linesInNeedle * 3:
    bestMatch = None
    for match in difflib.SequenceMatcher(a=needle, b=haystack).get_matching_blocks():
      if bestMatch is None or match.size > bestMatch.size:
        bestMatch = match
    # Bug - get_longest_match() doesn't always return the longest match - so we do it ourselfs.

    needleOffset = bestMatch.a
    haystackOffset = bestMatch.b
    sizeInChars = bestMatch.size

    a = max(0,haystack[0:haystackOffset].count("\n") - linesInNeedle)
    b = min(b, b - haystack[haystackOffset + sizeInChars:].count("\n") + linesInNeedle)


  while True:
    currentHs = "\n".join(hs[a:b])
    origMatcher = difflib.SequenceMatcher(a=needle, b=currentHs)
    sequence = origMatcher.get_opcodes()
    origScore = origMatcher.ratio()

    if len(currentHs) < len(needle) and origScore < 0.2:
      return (None,0)

    charsToMaybeAdvanceA = sequence[0][4]
    charsToMaybeReduceB = sequence[-1][4] - sequence[-1][3]

    if charsToMaybeAdvanceA == 0:
      linesToMaybeAdvnaceA = 1
    else:
      linesToMaybeAdvnaceA = currentHs[0:charsToMaybeAdvanceA].count("\n")
      if linesToMaybeAdvnaceA == 0: linesToMaybeAdvnaceA = 1
    
    if charsToMaybeReduceB == 0:
      linesToMaybeReduceB = 1
    else:
      linesToMaybeReduceB = currentHs[-charsToMaybeReduceB:].count("\n")
      if linesToMaybeReduceB == 0: linesToMaybeReduceB = 1


    moda = "\n".join(hs[a + linesToMaybeAdvnaceA:b])
    modb = "\n".join(hs[a:b - linesToMaybeReduceB])
    modab = "\n".join(
      hs[a + linesToMaybeAdvnaceA:b - linesToMaybeReduceB]) 
    
    d10r = ratio(needle, moda) 
    d01r = ratio(needle, modb) 
    d11r = ratio(needle, modab) 

    bestChoice = max([
      origScore,
      d01r,
      d10r,
      d11r,
      ])

    if bestChoice == 0.0: 
      return (None, 0)

    if bestChoice == origScore:
      if bestChoice > 0.6:
        return (currentHs, bestChoice)
      return (None, 0)
    
    elif bestChoice == d10r : a += linesToMaybeAdvnaceA
    elif bestChoice == d01r : b -= linesToMaybeReduceB
    elif bestChoice == d11r : a += linesToMaybeAdvnaceA; b -= linesToMaybeReduceB


def approximateSubStringByLineV1(needle : str, haystack : str):
  hs = haystack.splitlines()
  a = 0
  b = len(hs)

  while b - a > needle.count("\n") * 2 + 2:
    # This is a massive haystack - try divide and conquer
    # first

    halfB = int((a + b)/2)
    qtrB = a + int((b - a) /4)
    threeQtrB = a + int((b - a) * 3 /4)

    lString = "\n".join(hs[a:halfB])
    rString = "\n".join(hs[halfB:b])
    mString = "\n".join(hs[qtrB:threeQtrB])

    l = 1.0 if needle in lString else ratio(needle, lString)
    r = 1.0 if needle in rString else ratio(needle, rString)
    m = 1.0 if needle in mString else ratio(needle, mString)

    winner = max([l,r,m])

    if winner == l: b = halfB
    elif winner == m: a = qtrB; b = threeQtrB
    elif winner == r: a = halfB

  while True:
    d00 = "\n".join(hs[a + 0 : b - 0])
    d01 = "\n".join(hs[a + 0 : b - 1])
    d10 = "\n".join(hs[a + 1 : b - 0])
    d11 = "\n".join(hs[a + 1 : b - 1])
    #d02 = "\n".join(hs[a + 0 : b - 2])
    #d20 = "\n".join(hs[a + 2 : b - 0])
    #d22 = "\n".join(hs[a + 2 : b - 2])
    
    d00r = ratio(needle, d00) 
    d01r = ratio(needle, d01) 
    d10r = ratio(needle, d10) 
    d11r = ratio(needle, d11) 
    #d02r = ratio(needle, d02) 
    #d20r = ratio(needle, d20) 
    #d22r = ratio(needle, d22) 

    bestChoice = max([
      d00r,
      d01r,
      d10r,
      d11r,
      #d02r,
      #d20r,
      #d22r
      ])

    if bestChoice == 0.0: 
      return (None, 0)

    if bestChoice == d00r:
      if bestChoice > 0.6:
        return (d00, bestChoice)
      return (None, 0)
    
    elif bestChoice == d01r : b -= 1
    elif bestChoice == d10r : a += 1
    elif bestChoice == d11r : a += 1; b -= 1
    #elif bestChoice == d02r : b -= 2
    #elif bestChoice == d20r : a += 2
    #elif bestChoice == d22r : a += 2; b -= 2



def approximateSubString(needle : str, haystack : str):
  while True:
    dropFrontHalf = haystack[int(len(haystack)/2):]
    dropBackHalf  = haystack[:int(len(haystack)/2)]
    dropFront16   = haystack[16:]
    dropBack16    = haystack[:-16]
    dropFront1    = haystack[1:]
    dropBack1     = haystack[:-1]
    
    rDropFrontHalf = ratio(needle, dropFrontHalf)
    rDropBackHalf  = ratio(needle, dropBackHalf )
    rDropFront16   = ratio(needle, dropFront16  )
    rDropBack16    = ratio(needle, dropBack16   )
    rDropFront1    = ratio(needle, dropFront1   )
    rDropBack1     = ratio(needle, dropBack1    )

    rNoAction = ratio(needle, haystack)

    bestChoice = max([
      rNoAction,
      rDropFrontHalf,
      rDropBackHalf,
      rDropFront16,
      rDropBack16,
      rDropFront1,
      rDropBack1])

    if bestChoice == 0.0: 
      return (None, 0)

    if bestChoice == rNoAction:
      if bestChoice > 0.6:
        return (haystack, bestChoice)
      return (None, 0)
    elif bestChoice == rDropFrontHalf : haystack = dropFrontHalf
    elif bestChoice == rDropBackHalf  : haystack = dropBackHalf 
    elif bestChoice == rDropFront16   : haystack = dropFront16  
    elif bestChoice == rDropBack16    : haystack = dropBack16   
    elif bestChoice == rDropFront1    : haystack = dropFront1   
    elif bestChoice == rDropBack1     : haystack = dropBack1    


def bestMatchSubdivisionByLine(
  prefix : str, suffix : str, haystack : str):

  d = haystack.splitlines()

  linesExpected = 2 + prefix.count("\n") + suffix.count("\n")

  a = int(len(d) * prefix.count("\n") / linesExpected)

  while True:
    newPrefix = "\n".join(d[0:a])
    newSuffix = "\n".join(d[a:])

    current = (
      ratio(prefix, "\n".join(d[0:a])) + 
      ratio(suffix, "\n".join(d[a:])))

    aPlus1 = (
      ratio(prefix, "\n".join(d[0:a + 1])) + 
      ratio(suffix, "\n".join(d[a + 1:])))

    if a > 0:
      aTake1 = (
        ratio(prefix, "\n".join(d[0:a - 1])) + 
        ratio(suffix, "\n".join(d[a - 1 :])))
    else:
      aTake1 = 0

    bestChoice = max([
      current, aPlus1, aTake1])

    if bestChoice == 0: return (None, None)
    elif bestChoice == current: return a
    elif aPlus1 == bestChoice: a += 1  
    elif aTake1 == bestChoice: a -= 1



def bestMatchTripleSubdivisionByLine(
  prefix : str, middle : str, suffix : str, haystack : str):

  d = haystack.splitlines()

  linesExpected = 3 + prefix.count("\n") + middle.count("\n") + suffix.count("\n")

  a = int(len(d) * prefix.count("\n") / linesExpected)
  b = len(d) - int(len(d) * suffix.count("\n") / linesExpected)

  while True:
    newPrefix = "\n".join(d[0:a])
    newMiddle = "\n".join(d[a:b])
    newSuffix = "\n".join(d[b:])

    current = (
      ratio(prefix, "\n".join(d[0:a])) + 
      ratio(middle, "\n".join(d[a:b])) +
      ratio(suffix, "\n".join(d[b:])))

    aPlus1 = (
      ratio(prefix, "\n".join(d[0:a + 1])) + 
      ratio(middle, "\n".join(d[ a+ 1:b])) +
      ratio(suffix, "\n".join(d[b:])))

    if a > 0:
      aTake1 = (
        ratio(prefix, "\n".join(d[0:a - 1])) + 
        ratio(middle, "\n".join(d[a - 1:b])) +
        ratio(suffix, "\n".join(d[b:])))

      bothTake1 = (
        ratio(prefix, "\n".join(d[0:a - 1])) + 
        ratio(middle, "\n".join(d[a - 1:b - 1])) +
        ratio(suffix, "\n".join(d[b -1:])))
    else:
      aTake1 = 0
      bothTake1 = 0

    bPlus1 = (
      ratio(prefix, "\n".join(d[0:a])) + 
      ratio(middle, "\n".join(d[a:b+1])) +
      ratio(suffix, "\n".join(d[b+1:])))

    if a < b:
      bTake1 = (
        ratio(prefix, "\n".join(d[0:a])) + 
        ratio(middle, "\n".join(d[a:b-1])) +
        ratio(suffix, "\n".join(d[b-1:])))
    else:
      bTake1 = 0

    bothPlus1 = (
      ratio(prefix, "\n".join(d[0:a+1])) + 
      ratio(middle, "\n".join(d[a+1:b+1])) +
      ratio(suffix, "\n".join(d[b+1:])))

    bestChoice = max([
      current, aPlus1, aTake1, bPlus1, bTake1,
      bothPlus1, bothTake1])

    if bestChoice == 0: return (None, None)
    elif bestChoice == current: return (a, b)
    elif aPlus1 == bestChoice: a += 1  
    elif aTake1 == bestChoice: a -= 1
    elif bPlus1 == bestChoice: b += 1  
    elif bTake1 == bestChoice: b -= 1
    elif bothPlus1 == bestChoice: b += 1; a +=1
    elif bothTake1 == bestChoice: b -= 1; a -=1

