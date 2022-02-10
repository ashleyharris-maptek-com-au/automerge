
class DiffOverview:

  def __init__(self):
    self.regions = []
    self.inRegions = []
    self.outRegions = []

  def append(self, chunk):
    self.regions.append(chunk)

    if 'inLine' in chunk.__dict__:
      self.inRegions.append(chunk)

    if 'outLine' in chunk.__dict__:
      self.outRegions.append(chunk)

  def summarise(self) -> str:
    i = 0;
    j = 0;
    s = ""
    while True:
      if i == len(self.inRegions) and j == len(self.outRegions): break
      if i == len(self.inRegions):
        s += self.outRegions[j].summarise()
        s += "\n"
        j += 1
        continue
      if j == len(self.outRegions):
        s += self.inRegions[i].summarise()
        s += "\n"
        i += 1
        continue

      if self.inRegions[i] == self.outRegions[j]:
        s += self.inRegions[i].summarise()
        s += "\n"
        j += 1
        i += 1
        continue

      s += self.inRegions[i].summarise()
      s += "\n"
      s += self.inRegions[j].summarise()
      s += "\n"
      j += 1
      i += 1

    return s

