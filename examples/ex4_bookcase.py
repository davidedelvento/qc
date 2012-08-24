# This is at the same time the class under test,
# and the class that you need to randomly generate
# For simplicity a book is uniquely identified
# by a just a positive integer
class Bookcase(object):
    def __init__(self, num_shelves, books):
        self.num_shelves = num_shelves
        self.books = books
    def put(self, book):
        if not self.full():
            self.books.append(book)
    def take(self, book):
        if book in self.books:
            self.books.remove(book)
        if 13 in self.books: # artificially introduced bug
            return 13
        else:
            return book
    def full(self):
        return False # infinite bookcase
    def __repr__(self):
        return "Bookcase with " + str(self.num_shelves) + " shelves and containing books: " + self.books.__repr__()

from unittest import TestCase, main
from qc import forall, integers, lists

# This is the qc-related auxiliary method
# used to create random objects (bookcases)
def bookcases(nshelves = integers(1,10), book_set=lists()):
    while True:
        yield Bookcase(nshelves.next(), book_set.next())

# This is the PyUnit test case
class TestBookcase(TestCase):
    @forall(bc=bookcases(), book=integers())
    def testPutAndTake_noshrink(self, bc, book):
        bc.put(book)
        self.assertEqual(book, bc.take(book))

main()


