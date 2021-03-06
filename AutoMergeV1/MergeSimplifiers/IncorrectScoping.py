from Merge import Merge
import difflib, copy

def Process(merge : Merge) -> Merge:

  if merge.actual.strip() == "": return

  def score(a,b):
    return difflib.SequenceMatcher(None,a,b).ratio()

  m = copy.copy(merge)

  origScoreAE = score(m.actual, m.expected)
  origScoreAN = score(m.actual, m.new)
  
  lineMax = max(m.expected.count("\n"),
                m.new.count("\n"),
                m.suffix.count("\n"))
  lineMax = min(lineMax, 20) # Realistic limit.

  maxScore = max(origScoreAE, origScoreAN)
  maxLines = None

  lines = m.suffix.splitlines();

  for lineCount in range(0, lineMax):
    newActual = m.actual + "\n".join(lines[0:lineCount + 1])
    newSuffix = "\n".join(lines[lineCount + 1:])

    scoreAE = score(newActual, m.expected)
    scoreAN = score(newActual, m.new)

    if (scoreAE > maxScore or scoreAN > maxScore):
      maxScore = max(scoreAE, scoreAN)
      maxLines = lineCount

    if lineCount == 10 and maxLines is None:
      # Early exit on big diffs that aren't going anywhere after
      # a few lines
      return None

  if maxLines is not None and maxScore > 0.6:
    # We've improved the score by lengthening actual and shrinking suffix

    m = copy.copy(merge)
    newActual = m.actual + "\n".join(lines[0:maxLines + 1])
    newSuffix = "\n".join(lines[maxLines + 1:])

    m.actual = newActual
    m.suffix = newSuffix

    return m

  return None
