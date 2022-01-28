from Merge import Merge
import DiffSolver

def Solve(m : Merge):
  """
  Got a short merge that just isn't working?

  Try a few different ways of expressing it as a multi line
  sequence - we might make some progress, and then merge it back together.

  Split tokens on whitespace. Also pairs and triplets.

  Half a comment may match and merging may only need to be run on
  a few tokens.

  This also enables some useful "single word" merge strategies, that
  we may want to do.
  ie two edits changing a word to two different words - take the
  one thats... spelled correctly? Occurs elsewhere in the file?
  etc. etc.

  """

