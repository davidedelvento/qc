from qc import integers, floats, unicodes, characters, lists, tuples, dicts, objects, forall, qc_shrink, call_and_shrink
import math
from nose.tools import raises

# Integers

@forall(tries=10, i=integers())
def test_integers(i):
    assert type(i) == int, "expected an int, instead got a " + str(type(i))

@forall(tries=10, i=integers(low=0, high=100))
def test__nonnegative_integers(i):
    assert type(i) == int, "expected an int, instead got a " + str(type(i))
    assert 0 <= i <= 100, "not the expected range"

@forall(tries=10, i=integers(low=-100, high=0))
def test__nonpositive_integers(i):
    assert type(i) == int, "expected an int, instead got a " + str(type(i))
    assert -100 <= i <= 0, "not the expected range"

# Floats

@forall(tries=10, i=floats())
def test_floats(i):
    assert type(i) == float, "expected a float, instead got a " + str(type(i))

@forall(tries=10, i=floats(low=0, high=100))
def test_nonnegative_floats(i):
    assert type(i) == float, "expected a float, instead got a " + str(type(i))
    assert 0 <= i <= 100 or math.isnan(i) or math.isinf(i), "not the expected range"

@forall(tries=10, i=floats(low=-100, high=0))
def test_nonpositive_floats(i):
    assert type(i) == float, "expected a float, instead got a " + str(type(i))
    assert -100 <= i <= 0 or math.isnan(i) or math.isinf(i), "not the expected range"

@forall(tries=10, i=floats(low=-100, high=-100, special=False))
def test_nonspecial_floats(i):
    assert type(i) == float, "expected a float, instead got a " + str(type(i))
    assert -100 <= i <= 100, "not the expected range"

# Lists and tuples 

@forall(tries=10, l=lists(items=integers()))
def test_a_int_list(l):
    assert type(l) == list, "expected a list, instead got a " + str(type(l))
    for i in l:
        assert type(i) == int, "expected an int, instead got a " + str(type(i))

@forall(tries=10, t=tuples(items=integers()))
def test_a_int_tuple(t):
    assert type(t) == tuple, "expected a tuple, instead got a " + str(type(t))
    for i in t:
        assert type(i) == int, "expected an int, instead got a " + str(type(i))

@forall(tries=10, l=lists(items=floats()))
def test_a_float_list(l):
    assert type(l) == list, "expected a list, instead got a " + str(type(l))
    for i in l:
        assert type(i) == float, "expected a float, instead got a " + str(type(i))

@forall(tries=10, t=tuples(items=floats()))
def test_a_float_tuple(t):
    assert type(t) == tuple, "expected a tuple, instead got a " + str(type(t))
    for i in t:
        assert type(i) == float, "expected a float, instead got a " + str(type(i))

@forall(tries=10, l=lists(items=integers(), size=(10, 50)))
def test_lists_size(l):
    assert 10 <= len(l) <= 50, "list of unexpected size: " + str(len(l))

@forall(tries=10, t=tuples(items=integers(), size=(10, 50)))
def test_tuples_size(t):
    assert 10 <= len(t) <= 50, "tuple of unexpected size: " + str(len(t))

@raises(AssertionError)
@forall(tries=10, t=tuples(size=(-10, 10)))
def test_negative_tuples_size(t):
    pass # must raise an exception for negative sizes

@raises(AssertionError)
@forall(tries=10, t=lists(size=(-10, 10)))
def test_negative_lists_size(t):
    pass # must raise an exception for negative sizes

@raises(Exception)
@forall(tries=10, t=tuples(size=(20, 10)))
def test_wrong_tuples_size(t):
    pass # must raise an exception for min > max

@raises(Exception)
@forall(tries=10, t=lists(size=(20, 10)))
def test_wrong_lists_size(t):
    pass # must raise an exception for min > max

# Unicode and characters

@forall(tries=10, c=characters())
def test_characters(c):
    assert len(c) == 1

@forall(tries=10, ul=lists(items=unicodes()))
def test_unicodes_list(ul):
    assert type(ul) == list
    if len(ul):
        assert type(ul[0]) == unicode

@forall(tries=10, u=unicodes())
def test_unicodes(u):
    assert type(u) == unicode

@forall(tries=10, u=unicodes(size=(1,1)))
def test_unicodes_size(u):
    assert len(u) == 1

def random_int_unicode_tuple():
    i = integers()
    u = unicodes()
    while True:
        yield (i.next(), u.next())

@forall(tries=10, l=lists(items=random_int_unicode_tuple()))
def test_a_tupled_list(l):
    for x in l:
        assert type(x[0]) == int and type(x[1]) == unicode

# Other tests

@forall(tries=10, x=integers(), y=integers())
def test_integer_addition_commutative(x, y):
    assert x + y == y + x

@forall(tries=10, l=lists())
def test_reverse_reverse(l):
    assert list(reversed(list(reversed(l)))) == l

# Dictionaries

def kv_unicode_integers():
    u = unicodes()
    i = integers()
    while True:
        yield (u.next(), i.next())

@forall(tries=10, d=dicts(key_values=kv_unicode_integers()))
def test_dicts(d):
    for x, y in d.iteritems():
        assert type(x) == unicode
        assert type(y) == int

def kv_unicodes_lists():
    u = unicodes()
    l = lists()
    while True:
        yield (u.next(), l.next())

@forall(tries=10, d=dicts(key_values=kv_unicodes_lists(), size=(2, 2)))
def test_dicts_size(d):
    assert len(d) == 2
    for x, y in d.iteritems():
        assert type(x) == unicode
        assert type(y) == list

# Shrinking

def test_shrink_empty_list():
    empty_list_has_been_shrunk = False
    for x in qc_shrink([]):
        empty_list_has_been_shrunk = True
    assert empty_list_has_been_shrunk == False, "Empty lists must not be shrunk"

def test_shrink_single_element_list():
    repeated = False
    l = [0]
    for x in qc_shrink(l):
        if x == l:
            repeated = True
    assert repeated == False, "Shrink must not repeat things already seen"

@forall(full_l=lists())
def test_shrink_lists(full_l):
    for sub_l in qc_shrink(full_l):
        assert len(sub_l) <= len(full_l)/2 + 1

@forall(full_i=integers(low=-100))
def test_shrink_integers(full_i):
    for i in qc_shrink(full_i):
        assert abs(i) <= abs(full_i)/2 + 1
        assert cmp(i,0) == cmp(full_i, 0)   # shrink shall not change sign
        assert isinstance(i, int)

@forall(full_f=floats(low=-5.0, high=5.0))
def test_shrink_floats(full_f):
    for f in qc_shrink(full_f):
        if abs(full_f) > 1:
            assert abs(f) <= abs(full_f)/2 + 1
        else:
            assert abs(f) >= abs(full_f)/2 + 1
        assert cmp(f,0) == cmp(full_f, 0)   # shrink shall not change sign
        assert isinstance(f, float)

@forall(tries=10, i=integers(low=0, high=10))
def each_integer_from_0_to_10(i, target_low, target_high):
    assert i >= target_low and i<= target_high

def test_qc_partials():
    each_integer_from_0_to_10(target_low=0, target_high=10)


class TestClass(object):
    def __init__(self, arg):
        self.arg_from_init = arg

@forall(tries=10, obj=objects(TestClass, {'an_int': integers(), 'a_float': floats()}, unicodes()))
def test_objects(obj):
    assert type(obj) == TestClass
    assert type(obj.an_int) == int
    assert type(obj.a_float) == float
    assert type(obj.arg_from_init) == unicode

