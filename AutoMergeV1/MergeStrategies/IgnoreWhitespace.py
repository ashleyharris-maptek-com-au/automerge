from Merge import Merge
import re

def Solve(m : Merge):
  e = re.sub(R"\s", "", m.expected)
  a = re.sub(R"\s", "", m.actual)
  n = re.sub(R"\s", "", m.new)

  if a == e:
    # What's there and what we expected to be there were identical sans whitespace
    # apply the new change.
    return {m.new : 10}

  if n == e:
    # We were applying a whitespace change. Assume that this was via clangformat
    # or some other tool so can be repeated. Keep the actual as it has actual work.
    return {m.actual : 10}

  if n == a:
    # Two edits were done silmultainoulsy but were different in whitespace - 
    # apply ours.
    return {m.new : 10}

  return None

