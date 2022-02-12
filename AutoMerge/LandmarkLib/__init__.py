"""
Landmarks are a way of describing an area in text in such redundant
ways that we have a decent chance of finding the same spot in
a modified version of the text.

Eg:

  if "Total Defects" not in job["Review Details"]: continue
  if (job["Review Details"]X["Total Defects"] == 0): continue
  if (job['Repository Name'] != "mdf_products"): continue

A valid landmark sequence for X may be:
- 1. Between '"Review Details"]' and '["Total Defects"'
- 2. Longest line, between ']' and '['
- 3. After "if (job["Review Details"]"
- 4. Before ["Total
- 5. Before "["Total Defects"] == 0)"
- 6. Before ["Total Defects"] == 0): continue
- 7. After first "]" on line "if (job["Review Details"]["Total Defects"] == 0): continue"
- 8. After first "]" on line after "if "Total Defects" not in"
- 9. Before second "[" between lines "..." and "..."
- 10. Between "[" and "]", about 22 characters after first "if ("
- and many more.

If the text changes to:

  if "Total Defects" not in json["ReviewDetails"]: 
    continue
  if (json["ReviewDetails"]["TotalDefects"] == 0): 
    raise ValueError("Not defected enough!")
  if (json['RepositoryName'] != "mdf_products"): 
    raise ValueError("Wrong repository")

8 of the landmarks no longer exactly match, but #4 and #10 match to the 
"same spot", without any fuzzy matching. 4 additional rules should
fuzzily match reliably, and 4 more may match:

- 1. Should fuzzily match - only a single space was deleted
- 2. Should weak match - there are 2 equal longest lines but
     only one with the token set.
- 3. May fuzzily match.
- 4. Perfect match.
- 5. Should fuzzily match. Single deleted space.
- 6. May fuzzily match - deleted token and space
- 7. May fuzzily match - the closest line to the spec.
- 8. Wont match anything.
- 9. May fuzzily match the bounding lines - bit a stretch but may.
- 10. Exact match.

After running all these rules over the second text, the same location
should be found.

Landmarks are used in microdiffs to create selections for changes to
apply to. The above example was zero-width, but also supports non-zero
width selection.


"""

import LandmarkLib.LineSelection as _ls
import LandmarkLib.NeighbouringCharacterSelection as _cs

class LineSelector:
  def __init__(self):
    self.selectors = []

  def Search(lines : str):
    maxIndex, scores = _ls.ApplyLineSelectorsToContent(self.selectors, lines)

    return maxIndex

  def ScorePerLine(lines : str):
    maxIndex, scores = _ls.ApplyLineSelectorsToContent(self.selectors, lines)

    return scores


def DescribeLine(lines : list, lineIndex : int):
  selectors = _ls.FindAllLineSelectors(lines, lineIndex)

  lineSelector = LineSelector()
  lineSelector.selectors = selectors
  return lineSelector

class CharacterRangeSelector:
  def __init__(self):
    self.selectors = []

  def Search(lines : str) -> (int,int):
    pass

  def ScorePerChar(lines : str) -> (list,list):
    pass


def DescribeCharacterRange(string : str, begin : int, end : int):
  selectors = _cs.FindAllCharSelectors(string, begin, end)

  charSelector = CharacterRangeSelector()
  charSelector.selectors = selectors
  return charSelector

