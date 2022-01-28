from io import StringIO
import sys

class Merge(object):
  """description of class"""

  def __init__(self):
    self.prefix = ""
    self.actual = ""
    self.expected = ""
    self.new = ""
    self.suffix = ""
    self.actualHash = ""
    self.newHash = ""
    self.isValid = False

  def fromStream(self, stream):
    prefix = ""
    actual = ""
    expected = ""
    new = ""
    suffix = ""
    while True:
      line = stream.readline()
      if not line:
        print("No more merge markers!")
        return
      line = line.rstrip()
      if line.startswith("<<<<<<<"): break
      prefix += line
      prefix += "\n"
        
    if " " in line:
      marker, space, hash1 = line.partition(" ")
      if " " in hash1: hash1, space, commitName = hash1.partition(" ")
      self.actualHash = hash1

    while True:
      line = stream.readline().rstrip()
      if line is None: raise "Corrupt merge - no ||||";
      if line.startswith("|||||||"): break
      actual += line
      actual += "\n"
        
    while True:
      line = stream.readline().rstrip()
      if line is None: raise "Corrupt merge - no =======";
      if line.startswith("======="): break
      expected += line
      expected += "\n"
         
    while True:
      line = stream.readline().rstrip()
      if line is None: raise "Corrupt merge - no >>>>>>>"
      if line.startswith(">>>>>>>"): break
      new += line
      new += "\n"
        
    if " " in line:
      marker, space, hash2 = line.partition(" ")
      if " " in hash2: hash2, space, commitName = hash2.partition(" ")
      self.newHash = hash2

    while True:
      line = stream.readline()
      if not line: break
      suffix += line.rstrip()
      suffix += "\n"

    self.prefix = prefix
    self.actual = actual
    self.expected = expected
    self.new = new
    self.suffix = suffix
    self.isValid = True


  def fromString(self, text):
    self.fromStream(StringIO(text))

  def fromFile(self, path):
    self.fromStream(open(path))
