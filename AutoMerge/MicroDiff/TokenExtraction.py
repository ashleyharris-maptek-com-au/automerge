


"""
=# 

Represents an extraction of tokens into a named variable.

=Old

// Call our function
auto v = functionCall(a + (4 / b));

=New

constexpr auto c = a + (4 / b);

// Call our function
auto v = functionCall(c);

=Expect
Token extract "a", "+", "(", "4", "/", "b", ")"
from ["functionCall", "("][")",";"]
alias "c"
prefix ["constexpr", "auto"]
divider ["="]
appendix [";"]
"""

