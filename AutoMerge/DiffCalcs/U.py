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
