
class UnchangedRegion:
  def __init__(self) -> None:
    self.content = ""
    self.inLine = -1
    self.outLine = -1
    self.lineCount = 0

  def summarise(self) -> str:
    lineCount = self.content.count("\n")

    if lineCount <= 1: return "(unchanged line)"
    return "(" + str(lineCount) + " lines unchanged)"

