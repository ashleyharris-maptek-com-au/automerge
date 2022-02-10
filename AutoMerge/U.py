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
        operator.startswith("<=") or operator.startswith("&&") or
        operator.startswith("||") or operator.startswith("<<") or
        operator.startswith(">>") or operator.startswith("->") or
        operator.startswith("::")):

      tokens.append(operator[0:2])
      operator = operator[2:]
      continue

    if operator[0].isspace():
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
