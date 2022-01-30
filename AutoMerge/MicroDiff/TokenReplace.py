
"""
=# 

Represents the replacement of a token, or token sequence, with
another token or token sequence

=Old
#ifdef WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif // WINDOWS
=New
#ifdef COMPILE_FOR_WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif // COMPILE_FOR_WINDOWS
=Expect
Token replacement: 'WINDOWS' -> 'COMPILE_FOR_WINDOWS'
"""

