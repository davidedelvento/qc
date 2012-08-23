from qc import forall, unicodes

# This example is adapted from Scala's
# https://github.com/rickynils/scalacheck
# and we are pretending to test the string
# concatenation, slicing and the len builtin

@forall(tries=2000, a=unicodes(), b=unicodes())
def testStartswith(a, b):
    concat = a + b
    assert concat.startswith(a)

@forall(tries=10, a=unicodes(), b=unicodes())
def testConcatenation(a, b):
    concat = a + b
    # the following is meant to fail as an example of a failure
    assert len(concat) > len(a)
    assert len(concat) > len(b)

@forall(a=unicodes(), b=unicodes(), c=unicodes())
def testSubstring(a, b, c):
    concat = a + b + c
    start = len(a)
    stop = len(a) + len(b)
    assert concat[start: stop] == b


