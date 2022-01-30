

class ChangedRegion:
  def __init__(self) -> None:
    self.inContent = ""
    self.outContent = ""
    self.inLine = -1
    self.outLine = -1

  def summarise(self) -> str:
    lineCount = (
      self.inContent.count("\n") + self.outContent.count("\n")) / 2

    if lineCount <= 1: return "Changed a line"
    return "Changed " + str(lineCount) + " lines"

