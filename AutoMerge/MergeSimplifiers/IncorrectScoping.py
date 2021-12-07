from Merge import Merge
import difflib, copy

def Process(merge : Merge) -> Merge:

  def score(a,b):
    return difflib.SequenceMatcher(None,a,b).ratio()

  m = copy.copy(merge)

  origScoreAE = score(m.actual, m.expected)
  origScoreAN = score(m.actual, m.new)
  
  lineMax = max(m.expected.count("\n"),
                m.new.count("\n"),
                m.suffix.count("\n"))

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

  if maxLines is not None:
    # We've improved the score by lengthening actual and shrinking suffix

    m = copy.copy(merge)
    newActual = m.actual + "\n".join(lines[0:maxLines + 1])
    newSuffix = "\n".join(lines[maxLines + 1:])

    m.actual = newActual
    m.suffix = newSuffix

    return m

  return None

m = Merge()
m.prefix = """
void mdf::reeC_TreeSyncer::PostProcess(
  reeN_Commands::S_UpdateVisibilityTask& Cmd)
{
  reeN_Factory::WithRenderer([&](reeN_Cobalt::IRenderer* R)
  {
    for (auto r : Cmd.myRenderables)
    {
      auto& ri = myRenderableInfo[Tsize(r)];

      auto& bl = myBufferLayouts[Tsize(ri.myLayout)];
      auto& bg = bl.myBufferGroups[Tsize(ri.myBufferGroup)];

      for (auto& pl : ri.myPipelines)
      {
""".strip()

m.actual = """
bg.ForAllPipelineBuffers(pl, [&](S_BufferPipeline* ppdPtr)
""".strip()

m.expected = """
        auto& ppd = bg.myPerPipelineData[Tsize(pl)];

        if (ppd.myIndirectDrawBuffer && ppd.myShadowFirstChangedByte != -1)
""".strip()

m.new = """
        auto ppdPtr = bg.FindBufferPipeline(shadT_RenderModeId(0), shadT_RenderPassId(0), pl);
        ASSERT(ppdPtr);
        auto& ppd = *ppdPtr;

        if (ppd.myIndirectDrawBuffer && ppd.myShadowFirstChangedByte != -1)
        """.strip()

m.suffix = """
        {
          ASSERT(ppdPtr);
          auto& ppd = *ppdPtr;

          if (ppd.myIndirectDrawBuffer && ppd.myShadowFirstChangedByte != -1)
          {
            ppd.myIndirectDrawBuffer->QueueDataUpdate(
              ppd.myShadowDrawBuffer.data() + ppd.myShadowFirstChangedByte,
              ppd.myShadowLastChangedByte - ppd.myShadowFirstChangedByte,
              ppd.myShadowFirstChangedByte);

            ppd.myShadowFirstChangedByte = -1;
            ppd.myShadowLastChangedByte = 0;
          }
        });
      }
    }
  });
}
""".strip()

m2 = Process(m)

print(m2)