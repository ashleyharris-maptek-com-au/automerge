"""
MegaDiffs are first-pass diffs, these include things like:
- Chunks of code deleted
- Entirely new sections added
- A chunk of code remains unchanged
- A chunk of code has been changed, but is similar to what it was before. 
    (In some as yet undetermined way)
- A chunk of code is moved and changed, but remains similar 
- A chunk of code has been replaced with something radically different 
    to what was there before.

MegaDiff code can handle thousand line diffs - so, feel free to pipe git
commits into it.
"""

import DiffOverview
import UnchangedRegion
import ChangedRegion
import RewrittenRegion
import InsertedRegion
import DeletedRegion
import MovedRegion
import difflib

def Solve(old : str, new : str):
  oldArray = old.splitlines()
  newArray = new.splitlines()

  def tidy(a : str) -> str:
    return a.replace(" ").replace("\t").lower()

  oldStripedDown = [tidy(n) for n in oldArray]
  newStripedDown = [tidy(n) for n in oldArray]

  instructions = difflib.SequenceMatcher(
    a=oldStripedDown,b=newStripedDown).get_opcodes()

  inputLooseChunks = []
  outputLooseChunks = []

  # First pass - just unpack the sequence matcher stuff
  do = DiffOverview.DiffOverview()

  for (tag, i1, i2, j1, j2) in instructions:
    if tag == 'equal':

      old = "\n".join(oldArray[i1:i2]) + "\n" 
      new = "\n".join(newArray[i1:i2]) + "\n"

      if old == new:
        ucr = UnchangedRegion.UnchangedRegion()
        ucr.content = old
        ucr.inLine = i1
        ucr.outLine = j1
        ucr.lineCount = j2 - j1

        do.regions.append(ucr)
      else:
        # This is a very minor change - exclude it from move
        # detection as we know it's basically from here sans
        # capitalisation and spacing.

        cr = ChangedRegion.ChangedRegion()
        cr.inLine = i1
        cr.outLine = i2
        cr.inContent = old
        cr.outContent = new

        do.regions.append(cr)

    elif tag == 'replace':
      old = "\n".join(oldArray[i1:i2]) + "\n" 
      new = "\n".join(newArray[i1:i2]) + "\n"

      ratio = difflib.SequenceMatcher(a=old, b=new).ratio()

      if ratio < 0.4:
        # Assume total rewrite - anything on the old side
        # is totally gone. This can help with merge resolution
        # as anything changed in parallel with the rewrite is
        # lost. Also helps speed up diffs as we don't microdiff
        # these.
        cr = RewrittenRegion.RewrittenRegion()
        inputLooseChunks.append((old, cr))
        outputLooseChunks.append((new, cr))

      elif ratio < 0.6:
        # Not a total rewrite - but it may still be. Include it
        # for more detection just in case.
        cr = ChangedRegion.ChangedRegion()
        inputLooseChunks.append((old, cr))
        outputLooseChunks.append((new, cr))
      else:
        # This is pretty close to what was there before - don't
        # look for it in moves.
        cr = ChangedRegion.ChangedRegion()

      cr.inLine = i1
      cr.outLine = i2
      cr.inContent = old
      cr.outContent = new

      do.regions.append(cr)

    elif tag == 'insert':
      new = "\n".join(newArray[i1:i2]) + "\n"
      ir = InsertedRegion.InsertedRegion()
      ir.content = new
      ir.outLine = i1

      outputLooseChunks.append(
        (new, ir))

      do.regions.append(ir)

    elif tag == 'delete':
      new = "\n".join(newArray[i1:i2]) + "\n"

      dr = DeletedRegion.DeletedRegion()
      dr.content = new
      dr.inLine = i1

      inputLooseChunks.append(
        (old, dr))

      do.regions.append(dr)

  # TODO - look for duplicated chunks would go here...

  # Find any moved chunks
  while True:
    bestMatch = (None, None, 0)
    for i in inputLooseChunks:
      for o in outputLooseChunks:
        ratio = difflib.SequenceMatcher(a=i[0], b=o[0]).ratio()

        if ratio > bestMatch[2]:
          bestMatch = (i,0, ratio)

    if bestMatch[2] == 0: break

    if ratio < 0.5: break

    try: do.regions.remove(bestMatch[0][1])
    except: pass
    try: do.regions.remove(bestMatch[1][1])
    except: pass

    inputLooseChunks.remove(bestMatch[0])
    outputLooseChunks.remove(bestMatch[1])

    mc = MovedRegion.MovedRegion()
    mc.inContent = bestMatch[0][0]
    mc.outContent = bestMatch[1][0]
    mc.inLine = bestMatch[0][1].inLine
    mc.outLine = bestMatch[1][1].inLine

    do.regions.append(mc)

    crrr = [ChangedRegion.ChangedRegion,
            RewrittenRegion.RewrittenRegion]

    if isinstance(bestMatch[0][1], crrr):
      # We've removed a change because we've marked it as the
      # old side of the move. That means there is a missing
      # insert.
      ir = InsertedRegion.InsertedRegion()
      ir.content = bestMatch[0].content
      ir.outLine = bestMatch[0].outLine
      do.regions.append(ir)

    if isinstance(bestMatch[1][1], crrr):
      # We've removed a change because we've marked it as the
      # new side of the move. That means there is a missing
      # delete.
      ir = DeletedRegion.DeletedRegion()
      ir.content = bestMatch[1].content
      ir.outLine = bestMatch[1].inLine
      do.regions.append(ir)

  do.inRegions = list(filter(lambda x: 'inLine' in x, do.regions))
  do.outRegions = list(filter(lambda x: 'outLine' in x, do.regions))

  do.inRegions.sort(key = lambda x: x.inLine)
  do.outRegions.sort(key = lambda x: x.outLine)

  return do