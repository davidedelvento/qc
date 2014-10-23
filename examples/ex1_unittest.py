from unittest import TestCase, main
from qc import forall, unicodes

# This example is adapted from Scala's
# https://github.com/rickynils/scalacheck
# and we are pretending to test the string
# concatenation, slicing and the len builtin

class TestString(TestCase):
    @forall(tries=2000, a=unicodes(), b=unicodes())
    def testStartswith(self, a, b):
        concat = a + b
        self.assertTrue(concat.startswith(a))

    @forall(tries=10, a=unicodes(), b=unicodes())
    def testConcatenation(self, a, b):
        concat = a + b
        # the following is meant to fail as an example of a failure
        self.assertTrue(len(concat) > len(a))
        self.assertTrue(len(concat) > len(b))

    @forall(a=unicodes(), b=unicodes(), c=unicodes())
    def testSubstring(self, a, b, c):
        concat = a + b + c
        start = len(a)
        stop = len(a) + len(b)
        self.assertEqual(concat[start: stop], b)

if __name__ == "__main__":
    main() 

