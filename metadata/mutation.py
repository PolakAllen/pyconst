

"""
State mutations are often of interest when analyising programs

A state mutation finds all points of interaction with the requested object. Note
that all interaction points are listed, as python3 allows for no safe operation
(descriptors allow any get to potentially be a modifier, and sub operators could
modify the parent reguardless)

Mutation graphs are stored onto contexts.

Their use is to provide pointers to the con
"""
