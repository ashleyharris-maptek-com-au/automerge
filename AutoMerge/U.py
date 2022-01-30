import difflib, re

def Tokenise(s : str) -> list:
  return re.findall(r"\b\w+\b",s)

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
