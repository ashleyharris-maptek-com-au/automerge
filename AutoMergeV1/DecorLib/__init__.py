"""
Decors are pretty things done to strings, that need to be
detected, diffed, removed and applied.

Examples include comment characters in various programming
language, ascii art tables, indentation, lists, C++ end of
line macro escaping, line dividors, and more.

Each module in this package implements:
  - Detect(str) -> None or Decor class
  - Diff(decorA, decorB) -> None or DecorDiff class

Any Decor class implements:
  - __str__ - prints a summary
  - process(DecorDiff) - returns a modified Decor or None
  - apply(text) - return the decorated string, is possible
  - remove(text) - removes the decor from the string, if possible

Any DecorDiff implements:
  - __str__ prints a summary

For example:

=Analyse
################################################X
#                  Section 1                    #
#        A great example of decoration          #
#-----------------------------------------------X
=Summary
AsciiBox '#' '#' '-' '#' '#' '#' 'X' 'X' 72
AlignH C 70
=Removed
Section 1

A great example of decoration
=DiffWith
################################################X
#                  Section 2                    @
#            Difference right border            @
#-----------------------------------------------X
=DiffSummary
AsciiBox 3 '#'->'@'
=ApplyTo
Section 3A

A very nice example of decoration, no need to look closely.
=Expect
################################################X
#                  Section 3A                   @
# A very nice example of decoration, no need to @
#                 look closely.                 @
#-----------------------------------------------X
=#

Note that commenting and uncommenting is implemented as
a removal of a decoration:

=Analyse
  //GLint buffer = local::ToGl(Buffer);
  //::glReadBuffer(buffer);
=Summary
  AsciiBox '//'
=DiffWith
  GLint buffer2 = local::ToGl(Buffer2);
  ::glReadBuffer(buffer2);
=DiffSummary
-AsciiBox
=ApplyTo
  // HWND buffer = local::ToDirect3D(Buffer);
  // device->setCopyBuffer(buffer);
=Expect
  HWND buffer = local::ToDirect3D(Buffer);
  device->setCopyBuffer(buffer);
=#

Note that decorations can be nested.
=FromString
TreeList 123.abc.
AsciiBox '// ' 70
=#ApplyTo
This is the header
-This is a list item.
--This is a sub item.

-This is a list with a very long item that is longer than 70 characters long and may cause issues
-This is another list item.
=Expect
// This is the header
// 1. This is a list item.
//   1.a This is a sub item
// 
// 2. This is a list with a very long item that is longer than 70
//    characters long and may cause issues
// 3. This is another list item.

"""

