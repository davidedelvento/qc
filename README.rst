============
 QuickCheck
============

.. image:: https://travis-ci.org/davidedelvento/qc.png
   :target: https://travis-ci.org/davidedelvento/qc

Introduction
============

This framework does Random and Combinatorial Testing. It is a Python framework
inspired by Haskell's QuickCheck_ and Scala's scalacheck_ (not a port to Python
of those frameworks).

In Combinatorial Testing, `qc` provides a deterministic implementation of all-choices
(simply picks all the combinatorial choices of parameters) and all-pairs_
algorithms. All-choices simply tests all possible choice of input parameters, so it's
an exhaustive, but very slow technique when there are more than a few parameters with
more than a handful of possible values each. The all-pairs_ algorithm is very
clever and exponentially reduces the running time, while still guaranteeing that each
pair of input parameter is tested for each possible combination of values.

In Random Testing, `qc` provides many convenient ways of generating test cases, and
a very useful automatic test case reduction. The test case reduction uses binary search
to find a small, failing test case, very quickly.

.. _QuickCheck: http://hackage.haskell.org/package/QuickCheck
.. _scalacheck: https://github.com/rickynils/scalacheck
.. _all-pairs: https://en.wikipedia.org/wiki/All-pairs_testing

More on Random Testing
======================

Since Random Testing is not popular, you may want to
have a look at the following videos from Professor
John Regehr, University of Utah (less than 15 minutes total) if you are not
familiar with the technique:

* `Introduction to random testing <http://www.youtube.com/watch?v=cwhC19Fa_84>`_
* `Why random testing is good (1) <http://www.youtube.com/watch?v=PrJZ6144eeM>`_
* `Why random testing is good (2) <http://www.youtube.com/watch?v=btlfWwyzSXQ>`_
* `Why random testing is good (3) <http://www.youtube.com/watch?v=iw6BtJxPT8A>`_
* `Why random testing is good (4) <http://www.youtube.com/watch?v=QrLtkSdMDgw>`_

As you can see, Random Testing is not just randomly feeding your software a random
stream of bytes. It requires more thoughts. The `Udacity course on
testing`_ has units 3 and 4 entirely dedicated to Random Testing,
describing many things you need to know about Random Testing: how to
create valid, good, random test cases (3.25-26 and 4.5-15), mutators
(3.29), oracles (3.30-34), test case reduction (4.5-6), tradeoffs
(4.18-20), and more.  Random Testing is also mentioned elsewhere in
the class (and expected to be known in the final exam). It is very
worth watching (the introductory videos linked above are from this
class).

.. _Udacity course on testing: http://www.udacity.com/overview/Course/cs258/CourseRev/1

Installation
============

The easy, system-wide way (requires administrative privileges)::

    sudo pip install -e git://github.com/davidedelvento/qc.git#egg=qc

If you don't feel ready to commit for a whole system install of this library, or
simply don't have root access on your machine, just copy the ``qc`` directory 
and its content (as seen in https://github.com/davidedelvento/qc/tree/master/qc
at the moment the content is a mere ``__init__.py`` file) into the location of your choice.  
To make `qc` available to your programs you will have to set the
``PYTHONPATH`` environmental variable or have the ``qc`` directory as
a subdirectory of the tree where you are running (for details, see 
https://docs.python.org/2/tutorial/modules.html#the-module-search-path if you
use python 2 or https://docs.python.org/3/tutorial/modules.html#the-module-search-path
if you use python 3)


Examples
========

``examples/ex1_unittest.py`` and ``examples/ex1_nose.py``
    These examples provide a simple example (borrowed from scalacheck)
    on how to use this framework with Python native PyUnit framework
    (aka unittest module) and with the popular nose framework.  Just
    run ``python examples/example1_unittest.py`` or ``nosetests
    examples/example1_nose.py``. Pytest can also run the nose tests
    using ``py.test examples/example1_nose.py``.

``examples/ex2_choices_pairs.py`` TBD

``examples/ex3_airplane.py``
    Simple example on how to have qc generate your own custom (random)
    objects and how to use them in practice.

``examples/ex4_bookcase.py``
    A more elaborate example, showing the power of automatic shrinking
    and showing how to write your own shrinker. In this example you can
    see how qc automagically finds the root cause of the bug, compare
    the output with or without shrinking!


Known bugs
==========

See https://github.com/davidedelvento/qc/issues for a list of known
issues. 

One common problem when using automatic shrinking is running out
of stack space in the recursion process (the shrink algorithm call
itself several times to produce a smaller test case). This may happen
either if there is a bug in qc itself, or if there is a problem in
your test code. You will see an error like::

    RuntimeError: maximum recursion depth exceeded while calling a Python object

with a stack trace that shows the recursion tree of the shrinking
method calling itself. To understand what is happening, it is usually
useful to add the ``shrink=False`` option to the ``@forall`` decorator
of the affected test method. In very rare cases it may be necessary to
increase the stack depth with a call to
``sys.setrecursionlimit(NEWDEPTH)``, but do not do it until you
understand that it is really the case for your test. More often than
not, there will be a bug in your code (especially likely if you are
writing your first shrinker) or in qc.  Please report the
latter to https://github.com/davidedelvento/qc/issues


