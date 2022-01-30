"""
=# 

Insert a token, or sequence of tokens, at a given point.

=Old

// Call our function
auto v = functionCall(a + (4 / b));

=New

// Call our function
auto v = functionCall(nullptr, a + (4 / b));

=Expect
Token insertion ["nullptr", ","]
between "functionCall", "("
and "a", "+"
"""

