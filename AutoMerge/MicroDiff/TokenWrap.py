
"""
=# 

Represents a token, or token sequence, wrapped by other token
sequnces.

=Old
const auto activeSetting = "active";
if (preferenceValue == activeSetting)
{
=New
const auto activeSetting = "active";
if (translate(preferenceValue) == activeSetting)
{
=Expect
Suround "preferenceValue" with:
"translate", "(",
")"
"""

