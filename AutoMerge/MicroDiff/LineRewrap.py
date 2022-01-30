"""
=# 

Represents the rewrapping of a line.

=Old
functionCall(abc,
             def,
             ghi);
=New
functionCall(
  abc, def, ghi);
=Expect
Remove Line "#include <opengl.H>"
"""

