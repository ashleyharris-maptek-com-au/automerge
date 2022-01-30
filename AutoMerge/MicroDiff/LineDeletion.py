"""
=# 

Represents the deletion of a line.

=Old
#ifdef WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif
=New
#ifdef WINDOWS
#include <Windows.H>
#endif
=Expect
Remove Line "#include <opengl.H>"
"""

