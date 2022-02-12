"""
=# 

Represents the rewrapping of a line - ie moving around tabs, spaces, and newlines.

Note we don't have the ability to "re-apply" it - you should be using a tool like
clang-format after a merge resolution, and the ability to decode format, and re-appply it,
is beyond the scope of this tool.

=Old
functionCall(abc,
             def,
             ghi);
=New
functionCall(
  abc, def, ghi);
=Expect
"""

