


class DeletedRegion:
  def __init__(self) -> None:
    self.content = ""
    self.inLine = -1

  def summarise(self) -> str:
    lineCount = self.content.count("\n")

    if lineCount <= 1: return "Deleted a line"
    return "Deleted " + str(lineCount) + " lines"

