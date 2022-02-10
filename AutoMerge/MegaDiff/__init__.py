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

from collections import namedtuple
from re import DOTALL, escape
import DiffOverview
import UnchangedRegion
import ChangedRegion
import RewrittenRegion
import InsertedRegion
import DeletedRegion
import MovedRegion
import difflib
import itertools
from dataclasses import dataclass

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

"""

def Solve(old : str, new : str):
  oldArray = old.splitlines()
  newArray = new.splitlines()

  def tidy(a : str) -> str:
    return a.replace(" ", "").replace("\t", "").lower()

  oldStripedDown = [tidy(n) for n in oldArray]
  newStripedDown = [tidy(n) for n in newArray]

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

  do.inRegions = list(filter(lambda x: 'inLine' in x.__dict__, do.regions))
  do.outRegions = list(filter(lambda x: 'outLine' in x.__dict__, do.regions))

  do.inRegions.sort(key = lambda x: x.inLine)
  do.outRegions.sort(key = lambda x: x.outLine)

  return do

"""

def Solve(old : str, new : str):
  oldTokens = Tokenise(old)
  newTokens = Tokenise(new)

  maybeMatches = []

  for a,b,c in Triplewise(oldTokens):
    reg = re.compile(
      re.escape(a) + r"\W+?" +
      re.escape(b) + r"\W+?" +
      re.escape(c))

    allMatchesInOld = list(re.finditer(reg, old))
    allMatchesInNew = list(re.finditer(reg, new))

    if len(allMatchesInOld) == 0 or len(allMatchesInNew) == 0:
      continue

    if len(allMatchesInOld) == len(allMatchesInNew):
      for d,e in itertools.zip_longest(allMatchesInOld, allMatchesInNew):
        d0, d1 = d.span()
        e0, e1 = e.span()
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          dr = (d1 - d0) * r + d0
          er = (e1 - e0) * r + e0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))

    elif len(allMatchesInNew) == 1:
      e0, e1 = allMatchesInNew[0].span()
      for d in allMatchesInOld:
        d0, d1 = d.span()
        dr = (d1 - d0) * r + d0
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          er = (e1 - e0) * r + e0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))


    elif len(allMatchesInOld) == 1:
      d0, d1 = allMatchesInOld[0].span()

      for e in allMatchesInNew:
        e0, e1 = e.span()
        er = (e1 - e0) * r + e0
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          dr = (d1 - d0) * r + d0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))



  matches = sorted(maybeMatches)
  # newMatches = sorted(maybeMatches, key=lambda x: x[1])

  lineToLineMap = Dict0()

  for match in matches:
    oldLine = old[0:(match[0])].count("\n")
    newLine = new[0:(match[1])].count("\n")

    lineToLineMap[(oldLine,newLine)] += 1

  oL = old.splitlines()
  nL = new.splitlines()

  # for o,n in lineToLineMap.keys():
  #   print(o, "->", n, oL[o].ljust(80), nL[n])

  chunks = []

  remainingLines = list(range(0, len(nL)))

  @dataclass
  class Chunk:
    oldLow: int
    oldHi: int
    newLow: int
    newHi: int

  while len(lineToLineMap) > 0:
    maxKey = max(lineToLineMap, key=lineToLineMap.get)
    lineFromLow, lineToLow = maxKey
    lineFromHi, lineToHi = maxKey

    while True:
      options = (None, 0)

      if lineFromLow > 0 and lineToLow > 0:
        mf, mt = lineFromLow - 1, lineToLow - 1
        if StripEqualOrContained(oL[mf], nL[mt]) and mt in remainingLines: 
          options = 'sub11', 10

      if lineFromHi < len(oL) - 1 and lineToHi < len(nL) - 1:
        mf, mt = lineFromHi + 1, lineToHi + 1
        if StripEqualOrContained(oL[mf], nL[mt]) and mt in remainingLines: 
          options = 'add11', 10

      if lineFromLow > 0 and lineToLow > 0:
        mf, mt = lineFromLow - 1, lineToLow - 1
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'sub11', score

      if lineFromLow > 0:
        mf, mt = lineFromLow - 1, lineToLow
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'sub10', score

      if lineToLow > 0:
        mf, mt = lineFromLow, lineToLow - 1
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'sub01', score

      if lineFromHi < len(oL) - 1 and lineToHi < len(nL) - 1:
        mf, mt = lineFromHi + 1, lineToHi + 1
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'add11', score

      if lineToHi < len(nL) - 1:
        mf, mt = lineFromHi, lineToHi + 1
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'add01', score

      if lineFromHi < len(oL) - 1:
        mf, mt = lineFromHi + 1, lineToHi
        score = lineToLineMap[(mf, mt)]
        if score > options[1]: options = 'add10', score

      if options[0] is None:
        break

      if options[0] == 'sub11' or options[0] == 'sub10': lineFromLow -= 1
      if options[0] == 'sub11' or options[0] == 'sub01': lineToLow -= 1

      if options[0] == 'add11' or options[0] == 'add10': lineFromHi += 1
      if options[0] == 'add11' or options[0] == 'add01': lineToHi += 1

    keysToRemove = []
    for kf, kt in lineToLineMap.keys():
      if kt >= lineToLow and kt <= lineToHi:
        keysToRemove.append((kf, kt))

    for ll in range(lineToLow, lineToHi + 1):
      remainingLines.remove(ll)

    for k in keysToRemove:
      del lineToLineMap[k]

    chunk = Chunk(lineFromLow, lineFromHi, lineToLow, lineToHi)

    chunks.append(chunk)

  while True:
    a, b = NextIncrementingSequence(remainingLines)
    
    if a is None: break

    chunk = Chunk(None, None, a, b)

    for eChunk in chunks:
      oldText = nL[eChunk.newLow : eChunk.newHi + 1]
      newRange = [eChunk.newLow, eChunk.newHi]
      oldRange = [eChunk.newLow, eChunk.newHi]

      if newRange[1] == a - 1:
        newRange[1] = b
      elif newRange[0] == b + 1:
        newRange[0] = a

      if newRange == oldRange: continue

      newText = nL[newRange[0] : newRange[1] + 1]

      sourceText = oL[eChunk.oldLow : eChunk.oldHi + 1]

      prevScore = Ratio(
        "\n".join(sourceText),
        "\n".join(oldText))

      newScore = Ratio(
        "\n".join(sourceText),
        "\n".join(newText))

      if newScore > prevScore:

        eChunk.newLow, eChunk.newHi = newRange
        chunk = None
        break


    if chunk: chunks.append(chunk)

    aI = remainingLines.index(a)
    bI = remainingLines.index(b)

    del remainingLines[aI: bI + 1]


  # Can we extend any of the source areas to make them a closer match?
  for eChunk in chunks:

    if eChunk.oldHi is None: continue

    while True:

      newText = "".join(nL[eChunk.newLow : eChunk.newHi + 1])
      sourceText = "".join(oL[eChunk.oldLow : eChunk.oldHi + 1])

      scores = [0, 0, 0, 0, 0, 0, 0]

      scores[3] = RatioToken(sourceText, newText)

      if eChunk.oldLow > 3:
        maybeText = "".join(oL[eChunk.oldLow - 3 : eChunk.oldHi + 1])
        scores[0] = RatioToken(maybeText, newText)

      if eChunk.oldLow > 2:
        maybeText = "".join(oL[eChunk.oldLow - 2 : eChunk.oldHi + 1])
        scores[1] = RatioToken(maybeText, newText)

      if eChunk.oldLow > 1:
        maybeText = "".join(oL[eChunk.oldLow - 1 : eChunk.oldHi + 1])
        scores[2] = RatioToken(maybeText, newText)

      if eChunk.oldHi < len(oL) - 1:
        maybeText = "".join(oL[eChunk.oldLow : eChunk.oldHi + 2])
        scores[4] = RatioToken(maybeText, newText)

      if eChunk.oldHi < len(oL) - 2:
        maybeText = "".join(oL[eChunk.oldLow : eChunk.oldHi + 3])
        scores[5] = RatioToken(maybeText, newText)

      if eChunk.oldHi < len(oL) - 3:
        maybeText = "".join(oL[eChunk.oldLow : eChunk.oldHi + 4])
        scores[6] = RatioToken(maybeText, newText)

      maxScores = max(scores)

      if maxScores == scores[3]: break

      if maxScores == scores[0]:
        eChunk.oldLow -= 3
      elif maxScores == scores[1]:
        eChunk.oldLow -= 2
      elif maxScores == scores[2]:
        eChunk.oldLow -= 1
      elif maxScores == scores[4]:
        eChunk.oldHi += 1
      elif maxScores == scores[5]:
        eChunk.oldHi += 2
      elif maxScores == scores[6]:
        eChunk.oldHi += 3


  # Now find which lines got toally removed
  unusedOldLines = list(range(0,len(oL)))
  usedTwiceOldLines = set()

  for c in chunks:
    if c.oldHi is None: continue
    for l in range(c.oldLow, c.oldHi + 1):
      if l in unusedOldLines:
        unusedOldLines.remove(l)
      else:
        usedTwiceOldLines.add(l)

  do = DiffOverview.DiffOverview()

  while True:
    a, b = NextIncrementingSequence(unusedOldLines)
    if a is None: break

    dr = DeletedRegion.DeletedRegion()
    dr.content = "\n".join(oL[a:b + 1])
    dr.inLine = a

    if dr.content.strip() != "":
      do.append(dr)

  for c in chunks:
    print('-' * 160)

    if c.oldLow is None:
      # Insertion:

      iR = InsertedRegion.InsertedRegion()
      iR.content = "\n".join(nL[c.newLow : c.newHi + 1])
      iR.outLine = c.newLow

      do.append(iR)

      for n in range(c.newLow, c.newHi + 1):
        ol = " " * 80
        nl = nL[n]

        print(None, "->", n, ol , nl)
    else:
      oldText = "\n".join(oL[c.oldLow : c.oldHi + 1])
      newText = "\n".join(nL[c.newLow : c.newHi + 1])

      if oldText == newText:
        ucr = UnchangedRegion.UnchangedRegion()
        ucr.content = oldText
        ucr.lineCount = c.newHi - c.newLow 
        ucr.inLine = c.oldLow
        ucr.outLine = c.newLow
        do.append(ucr)
      else:

        ratio = RatioToken(oldText, newText)

        if ratio < 0.2:
          rr = RewrittenRegion.RewrittenRegion()
          rr.inContent = oldText
          rr.outContent = newText
          rr.inLine = c.oldLow
          rr.outLine = c.newLow
          do.append(rr)
        else:
          cr = ChangedRegion.ChangedRegion()
          cr.inContent = oldText
          cr.outContent = newText
          cr.inLine = c.oldLow
          cr.outLine = c.newLow
          do.append(cr)

      for o,n in itertools.zip_longest(range(c.oldLow, c.oldHi + 1),
                                       range(c.newLow, c.newHi + 1)):

        ol = " " * 80
        if o: ol = oL[o].ljust(80)

        nl = ""
        if n: nl = nL[n]

        print(o, "->", n, ol , nl)


  do.inRegions.sort(key = lambda x: x.inLine)
  do.outRegions.sort(key = lambda x: x.outLine)

  return do



if __name__ == '__main__':
  test1 = """
std::vector<sgC_PickInformation> sgC_SceneView::GetObjectPickHits(
  Tint32s X,
  Tint32s Y,
  Tfloat64 PickRadius,
  picE_PickConsistency Consistency,
  reeC_FrustumInformation* FrustumInfo)
{
  // :NYI: Ryan Marker 2018-Jul-16 Being able to pick from a custom viewpoint
  // would be a useful feature, but while the API has been updated to reflect
  // this it still needs to be implemented. See EL-5983.
  if (FrustumInfo) ASSERT_NYI();

  std::vector<sgC_PickInformation> pickResults;

  const Tfloat64 pickRadiusSquared = PickRadius * PickRadius;

  const geoS_Extent2D regionS(geoS_Point2D(X - PickRadius, Y - PickRadius),
                              geoS_Point2D(X + PickRadius, Y + PickRadius));

  auto renderLambda = [&pickResults,
                       Consistency,
                       X,
                       Y,
                       PickRadius,
                       pickRadiusSquared,
                       FrustumInfo,
                       this,
                       regionS]()
  {
    if (!mySolidColourColourReader)
    {
      mySolidColourColourReader = mySolidColourFramebufferPtr->AddPixelReader(
        "mySolidColourColourReader");
    }
    if (!mySolidColourDepthReader)
    {
      mySolidColourDepthReader = mySolidColourFramebufferPtr->AddPixelReader(
        "mySolidColourDepthReader");
    }

    cmrS_Viewport viewport;
    Tbool cached = false;
    {
      thdC_LockR<S_SharedState> lockR(&mySharedState);

      viewport = lockR->myViewport;
      cached = lockR->isSolidColourFramebufferCached;
    }

    // :TRICKY: Ryan Marker 2017-Jul-19 Even though the cached size of the
    // framebuffers should be updated to be the same as the viewport; there
    // is a tiny chance when the view has just been resized where this isn't
    // the case. If this situation should occur then invalidate the cache so
    // that it is updated.
    if (mySolidColourColourReader->Width() != viewport.WidthS() ||
        mySolidColourColourReader->Height() != viewport.HeightS() ||
        mySolidColourDepthReader->Width() != viewport.WidthS() ||
        mySolidColourDepthReader->Height() != viewport.HeightS())
    {
      cached = false;
    }
"""

  test2 = """
std::vector<sgC_PickInformation> sgC_SceneView::GetObjectPickHits(
  Tint32s X,
  Tint32s Y,
  Tfloat64 PickRadius,
  picE_PickConsistency Consistency,
  reeC_FrustumInformation* FrustumInfo)
{
  // :NYI: Ryan Marker 2018-Jul-16 Being able to pick from a custom viewpoint
  // would be a useful feature, but while the API has been updated to reflect
  // this it still needs to be implemented. See EL-5983.
  if (FrustumInfo) ASSERT_NYI();

  std::vector<sgC_PickInformation> pickResults;

  auto renderLambda =
    [&pickResults, Consistency, X, Y, PickRadius, FrustumInfo, this](
      reeN_Cobalt::IRenderer* RendererLock)
    {
      auto gpuPick = PickInternals(X, Y, PickRadius);

      //:TODO: This is a really dumb first picking approach - this doesn't
      // attempt to resolve depth or find the most pixels "winner" or closest
      // or anything yet. I'm just proving the concept.
      if (gpuPick.myPickIdsCountAndMinMaxDepthTuples[0][0] > 0)
      {
        gbT_DataSetId uniqueId(
          gpuPick.myPickIdsCountAndMinMaxDepthTuples[0][0]);
        auto groupId = sgC_Node::ToGroupId(uniqueId);

        pickResults.push_back(sgC_PickInformation(0, 1, groupId, uniqueId));
      }
    };


  // const Tfloat64 pickRadiusSquared = PickRadius * PickRadius;

  // const geoS_Extent2D regionS(geoS_Point2D(X - PickRadius, Y - PickRadius),
  //                            geoS_Point2D(X + PickRadius, Y + PickRadius));

  // auto renderLambda = [&pickResults,
  //                     Consistency,
  //                     X,
  //                     Y,
  //                     PickRadius,
  //                     pickRadiusSquared,
  //                     FrustumInfo,
  //                     this,
  //                     regionS]()
  //{
  //  if (!mySolidColourColourReader)
  //  {
  //    mySolidColourColourReader =
  //    mySolidColourFramebufferPtr->AddPixelReader(
  //      "mySolidColourColourReader");
  //  }
  //  if (!mySolidColourDepthReader)
  //  {
  //    mySolidColourDepthReader = mySolidColourFramebufferPtr->AddPixelReader(
  //      "mySolidColourDepthReader");
  //  }

  //  cmrS_Viewport viewport;
  //  Tbool cached = false;
  //  {
  //    thdC_LockR<S_SharedState> lockR(&mySharedState);

  //    viewport = lockR->myViewport;
  //    cached = lockR->isSolidColourFramebufferCached;
  //  }

  //  // :TRICKY: Ryan Marker 2017-Jul-19 Even though the cached size of the
  //  // framebuffers should be updated to be the same as the viewport; there
  //  // is a tiny chance when the view has just been resized where this isn't
  //  // the case. If this situation should occur then invalidate the cache so
  //  // that it is updated.
  //  if (mySolidColourColourReader->Width() != viewport.WidthS() ||
  //      mySolidColourColourReader->Height() != viewport.HeightS() ||
  //      mySolidColourDepthReader->Width() != viewport.WidthS() ||
  //      mySolidColourDepthReader->Height() != viewport.HeightS())
  //  {
  //    cached = false;
  //  }
"""

  do = Solve(test1, test2)

  print(do.summarise())