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
        return False # This bookcase has infinite capacity
    def __repr__(self):
        return "Bookcase with " + str(self.num_shelves) + " shelves and containing books: " + self.books.__repr__()

from unittest import TestCase, main
from qc import forall, integers, lists, qc_shrink

# This is the qc-related auxiliary method
# used to create random objects (bookcases)
def bookcases(nshelves = integers(1,10), book_set=lists()):
    while True:
        yield Bookcase(nshelves.next(), book_set.next())

# This is the custom shrinking function we have to provide
# to qc. It has to decide the logic by which we want the
# test case to be shrunk. In this case, we just shrink
# the list of books, using qc default's shrink function.
# Note that we are not shrinking the number of shelves.
# This is the common pattern to create custom shrinker:
# decide what has to change and what has not. Call
# qc's shrinker on the relevant objects (if they are
# supported, otherwise write your own shrinker for those)
def shrink_bookcase(bookcase):
    if isinstance(bookcase, Bookcase):
        for shrinked_books in qc_shrink(bookcase.books):
            yield Bookcase(bookcase.num_shelves, shrinked_books)
    # else we do not shrink

# This is the PyUnit test case
class TestBookcase(TestCase):
    @forall(bc=bookcases(), book=integers())
    def testPutAndTake_noshrink(self, bc, book):
        bc.put(book)
        self.assertEqual(book, bc.take(book))

    @forall(bc=bookcases(), book=integers(), custom_shrink=shrink_bookcase)
    def testPutAndTake_shrink(self, bc, book):
        bc.put(book)
        self.assertEqual(book, bc.take(book))

main()


