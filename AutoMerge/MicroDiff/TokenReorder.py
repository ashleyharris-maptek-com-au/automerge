

"""
=# 

Represents reordering of the token sequence.

=Old

a = b + 2
c = d + 4

=New

a = d + b + 2
c = 4

=Expect
Token move: ["d", "+"] 
from ["c", "="],['4'] 
to ["a", "="],["b", "+"]
"""

