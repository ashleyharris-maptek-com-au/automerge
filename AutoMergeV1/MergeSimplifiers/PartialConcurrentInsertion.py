from Merge import Merge
import difflib, copy

def Process(merge : Merge) -> Merge:

  m = copy.copy(merge)

  if m.expected.strip() != "": return None
    
  anyChange = False

  while True:
    actFl, actNl, actRest = m.actual.partition("\n")
    newFl, newNl, newRest = m.new.partition("\n")

    if actFl.strip() == newFl.strip():
      m.actual = actRest
      m.new = newRest
      m.prefix += actFl
      m.prefix += "\n"
      anyChange = True
    else:
      break

  while True:
    actRest, actNl, actLl = m.actual.rpartition("\n")
    newRest, newNl, newLl = m.new.rpartition("\n")

    if actLl.strip() == newLl.strip():
      m.actual = actRest
      m.new = newRest
      m.suffix = actLl + "\n" + m.suffix
      anyChange = True
    else:
      break

  if anyChange: return m
  return None

