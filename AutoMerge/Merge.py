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

  def fromString(self, text):
    self.fromStream(StringIO(text))

  def fromFile(self, path):
    self.fromStream(open(path))
