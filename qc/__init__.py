# Copyright (c) 2009-2011, Dan Bravender <dan.bravender@gmail.com>
# Copyright (c) 2012-2014, Davide Del Vento <davide.del.vento @ gmail>

import random
import os, sys
import functools

def integers(low=0, high=100):
    '''Endlessly yields random integers between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    while True:
        yield random.randint(low, high)

def floats(low=0.0, high=100.0):
    '''Endlessly yields random floats between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    while True:
        yield random.uniform(low, high)

def lists(items=integers(), size=(0, 100)):
    '''Endlessly yields random lists varying in size between size[0]
       and size[1]. Yields a list of the low size and the high size
       first to test boundary conditions.
    '''
    yield [items.next() for _ in xrange(size[0])]
    yield [items.next() for _ in xrange(size[1])]
    while True:
        yield [items.next() for _ in xrange(random.randint(size[0], size[1]))]

def tuples(items=integers(), size=(0, 100)):
    '''Endlessly yields random tuples varying in size between size[0]
       and size[1]. Yields a tuple of the low size and the high size
       first to test boundary conditions.
    '''
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
        if abs(something) >= 2:
            yield something/2
    except TypeError:
        pass

def call_and_shrink(f, tryshrink, seed, custom_shrink, *inargs, **random_kwargs):
    try:
        f(*inargs, **random_kwargs)
    except AssertionError, e:     # shrink only when there is AssertionErrors, in other cases is ad infinitum recursion
        if tryshrink:
            for k in random_kwargs:
                for s in custom_shrink(random_kwargs[k]):
                    shrinked_kwargs = random_kwargs.copy()
                    shrinked_kwargs[k] = s
                    call_and_shrink(f, tryshrink, seed, custom_shrink, *inargs, **shrinked_kwargs)
        if sys.version_info[0] < 3:
            raise e.__class__("%s, generated with seed %s, caused a FAIL\n%s" %
                                  (random_kwargs, seed, e)), None, sys.exc_traceback
        else:
            raise e.__class__("{0}, generated with seed {1}, caused a FAIL\n".format(
                                   random_kwargs, seed)).with_traceback(e.__traceback__)

def forall(tries=100, shrink=True, seed=None, custom_shrink=qc_shrink, **kwargs):
    if seed is None:
        try:
            seed = hash(os.urandom(16))
        except NotImplementedError, e:
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
                    pprint(random_kwargs)
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
