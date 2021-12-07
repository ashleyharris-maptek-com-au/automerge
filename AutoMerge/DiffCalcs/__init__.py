"""
Diffs are a transition between 2 strings. For example:

=Old
  if (ReadFramebufferId)
  {
    ::glBindFramebuffer(GL_FRAMEBUFFER, 0);
  }
=New
  if (ReadFramebufferId) 
    ::glBindFramebuffer(GL_FRAMEBUFFER, 1);
=Summary
  Remove '{' and '}'
  Replace '0' with '1'
=#

These are designed in such a way that they can be replayed on variations
of the source string.

=ApplyTo
  if (isConnected && ReadFramebufferId)
  {
    ::glBindFramebuffer(GL_FRAMEBUFFER, 0);
  }
=Expect
  if (isConnected && ReadFramebufferId) 
    ::glBindFramebuffer(GL_FRAMEBUFFER, 1);
=#

Each module needs to impliment a "Process(old : str, new : str)" method, 
this should return a diff object which encapsulates at least part of the 
conversion from old to new. If it can't improve, or the technique doesn't
apply to such a difference, it should return None

The diff object needs to impliment an "applyTo(text)" method, which returns the
text argument, modified by the diff if possible.

"""

import pkgutil

allDiffGenerators = []

for a in pkgutil.iter_modules(['DiffCalcs']):
  exec("from DiffCalcs import " + a.name + " as t")

  if "Process" in dir(t):
    allDiffGenerators.append(t.Process)

