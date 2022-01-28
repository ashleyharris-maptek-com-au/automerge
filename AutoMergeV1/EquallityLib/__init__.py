"""
EquallityLib offers ways to match "identical" chunks of text. 

Identical is in the eye of the beholder, so each can be turned on or off
by config settings.

Examples include:
- Ignore all leading and trailing whitespace
- python friendly "respect indent but ignore it inside brackets"
- Match C-style statements wrapped differently
- Ignore all comments
- Ignore all case

EqualityClasses that are enabled implement 1 of 2 methods:
- Sanitise(text) method, this converts text into a form in which == would 
  correctly match the input - eg "ignore trailing whitespace" would just 
  return text.rstrip(). 
  
  This needs to be acceptable if it makes it into the final merge output,
  so "Ignore comments" would remove comments - this is probably undesirable
  in all cases.

  For code bases with tooling like ClangFormat, converting C++ statements
  to single lines is probably fine if ClangFormat can wrap them nicely
  afterwards - so ignore line breaks and indentation can be implemented by
  slurping multi line statements into single line ones.

- CompareSubstring(A : str, B : str) method. This returns:
  True if equal (under your definition of equal)
  False if not equal, or so distant it's not worth computing a diff.
  An array of DiffLib.Match objects when two strings are approximately equal,
  this array may have a single Match object if A is in B or B is in A.
  

"""
