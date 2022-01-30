

class InsertedRegion:
  def __init__(self) -> None:
    self.content = ""
    self.outLine = -1


  def summarise(self) -> str:
    lineCount = self.content.count("\n")

    if lineCount <= 1: return "Inserted a line"
    return "Inserted " + str(lineCount) + " lines"