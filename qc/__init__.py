# Copyright (c) 2009-2011, Dan Bravender <dan.bravender@gmail.com>
# Copyright (c) 2012-2014, Davide Del Vento <davide.del.vento @ gmail>

import random, math
import os, sys
import functools

def integers(low=-sys.maxint-1, high=sys.maxint):
    '''Endlessly yields random integers between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    for i in (-1,0,1):
        if low < i < high:
            yield i
    while True:
        yield random.randint(low, high)

def floats(low=-sys.float_info.max, high=sys.float_info.max, special=True):
    '''Endlessly yields random floats between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield float(low)
    yield float(high)
    for i in (-1.0, -sys.float_info.min, 0.0, sys.float_info.min, 1.0):
        if low < i < high:
            yield i
    if special:
        yield float('nan')
        yield float('inf')
        yield float('-inf')

    if low == -sys.float_info.max and high == sys.float_info.max:
        while True:   # uniform does not work for such a large range
            yield random.uniform(-2, 2) * 10 ** random.randint(-sys.float_info.max_10_exp+1, sys.float_info.max_10_exp-1)
    else:
        while True:   # TODO it should probably detect a large range and use an approach similar to the previous one
            yield random.uniform(low, high)

def lists(items=integers(), size=(0, 100)):
    '''Endlessly yields random lists varying in size between size[0]
       and size[1]. Yields a list of the low size and the high size
       first to test boundary conditions.
    '''
    assert size[0] >=0, "list size must be non-negative" 
    yield [items.next() for _ in xrange(size[0])]
    yield [items.next() for _ in xrange(size[1])]
    while True:
        yield [items.next() for _ in xrange(random.randint(size[0], size[1]))]

def tuples(items=integers(), size=(0, 100)):
    '''Endlessly yields random tuples varying in size between size[0]
       and size[1]. Yields a tuple of the low size and the high size
       first to test boundary conditions.
    '''
    assert size[0] >=0, "tuple size must be non-negative" 
    yield tuple([items.next() for _ in xrange(size[0])])
    yield tuple([items.next() for _ in xrange(size[1])])
    while True:
        yield tuple([items.next() for _ in xrange(random.randint(size[0], size[1]))])

def key_value_generator(keys=integers(), values=integers()):
    while True:
        yield [keys.next(), values.next()]

def dicts(key_values=key_value_generator(), size=(0, 100)):
    while True:
        x = {}
        for _ in xrange(random.randint(size[0], size[1])):
            item, value = key_values.next()
            while item in x:
                item, value = key_values.next()
            x.update({item: value})
        yield x

def unicodes(size=(0, 100), minunicode=0, maxunicode=255):
    for r in (size[0], size[1]):
        yield unicode('').join(unichr(random.randint(minunicode, maxunicode)) \
                for _ in xrange(r))
    while True:
        yield unicode('').join(unichr(random.randint(minunicode, maxunicode)) \
                for _ in xrange(random.randint(size[0], size[1])))

characters = functools.partial(unicodes, size=(1, 1))

def objects(_object_class, _fields={}, *init_args, **init_kwargs):
    ''' Endlessly yields objects of given class, with fields specified
        by given dictionary. Uses given constructor arguments while creating
        each object.
    '''
    while True:
        ctor_args = [arg.next() for arg in init_args]
        ctor_kwargs = (dict((k, v.next()) for k, v in init_kwargs.iteritems()))
        obj = _object_class(*ctor_args, **ctor_kwargs)
        for k, v in _fields.iteritems():
            setattr(obj, k, v.next())
        yield obj

def qc_shrink(something):
    try:
        if len(something) == 0:    # never shrink a zero-len object, since it
            return                 # will lead to infinite recursion
        if len(something) == 1:    # if single-object collection
            yield something[:0]    # try the empty collection
            return                 # if it works, no need to try the single-object
                                   # collection again
        l = len(something)/2
        yield something[:l]
        yield something[l:]
    except TypeError:
        pass
    try:
        if abs(something) >= 2 and not math.isinf(something):
            yield something/2
    except TypeError:
        pass

class QCAssertionError(AssertionError):
    def __init__(self, error, *args, **kwargs):
        super(QCAssertionError, self).__init__(*args, **kwargs)
        self.parent_error=error

    def __str__(self):
        return self.message + str(self.parent_error)

def call_and_shrink(f, tryshrink, seed, custom_shrink, *inargs, **random_kwargs):
    try:
        f(*inargs, **random_kwargs)
    except AssertionError as e:     # shrink only when there is AssertionErrors, in other cases is ad infinitum recursion
        if tryshrink:
            for k in random_kwargs:
                for s in custom_shrink(random_kwargs[k]):
                    shrinked_kwargs = random_kwargs.copy()
                    shrinked_kwargs[k] = s
                    if forall.verbose or os.environ.has_key('QC_VERBOSE'):
                        from pprint import pprint
                        pprint(random_kwargs)
                    call_and_shrink(f, tryshrink, seed, custom_shrink, *inargs, **shrinked_kwargs)
        if sys.version_info[0] < 3:
            raise QCAssertionError(e, str(random_kwargs) + 
                                      " (from seed " +str(seed) +  ") caused a FAIL: "), None, sys.exc_traceback
        else:
            raise QCAssertionError(e, "{0}, from seed {1}, caused a FAILURE\n".format(
                                   random_kwargs, seed)).with_traceback(e.__traceback__)

def forall(tries=100, shrink=True, seed=None, custom_shrink=qc_shrink, **kwargs):
    if seed is None:
        try:
            seed = hash(os.urandom(16))
        except NotImplementedError:
            seed = random.random()
    random.seed(seed)
    def wrap(f):
        @functools.wraps(f)
        def wrapped(*inargs, **inkwargs):
            for _ in xrange(tries):
                random_kwargs = (dict((name, gen.next())
                                 for (name, gen) in kwargs.iteritems()))
                if forall.verbose or os.environ.has_key('QC_VERBOSE'):
                    from pprint import pprint
                    pprint("Shrink history:")
                random_kwargs.update(**inkwargs)
                call_and_shrink(f, shrink, seed, custom_shrink, *inargs, **random_kwargs)
            if forall.printsummary:
                from pprint import pprint
                pprint(f.__name__+": passed "+str(tries)+" tests [OK]")
        return wrapped
    return wrap
forall.printsummary = False
forall.verbose = False # if enabled will print out the random test cases

__all__ = ['integers', 'floats', 'lists', 'tuples', 'unicodes', 'characters', 'objects', 'forall']
