# Location is a (lame) class needed by the
# class under test. In real life it will be
# a non-lame object you really need
class Location(object):
    def __init__(self, lat, lon, height):
        self.lat=lat
        self.lon=lon
        self.h=height

# This is the class under test
class Plane(object):  
    def __init__(self):
        self.location = Location(46.22, -112.1, 4968)
    def fly_to(self, loc):
        if (-75 < loc.lon < -70 and
             20 < loc.lat <  30 and
            loc.h < 6000):
            raise Exception("Plane has disappeared in the Bermuda triangle")
        else:
            self.location = loc
    def has_gas(self):
        return True

from unittest import TestCase, main
from qc import forall, floats

# This is the qc-related auxiliary method
# used to create random objects. In this
# simple example it is overkill, but the
# purpose here is just to show how it is
# done: in real life you may have several
# testing methods requiring random locations
# and defining the method this way will
# allow @forall to be able to inject 
# Location's everywhere you need them
def locations(lat = floats(-90,+90),
              lon = floats(-180, +180),
              height = floats(0, 30000)):
    while True:
        yield Location(lat.next(), lon.next(), height.next())


# This is the PyUnit test case
# In this example we are just
# flying the plane to random locations
# and assert that it does not run out
# of gas. In real life you would assert
# that it *does* run out of gas, but it
# does *not* fall apart in other ways.
class TestPlane(TestCase):
    def setUp(self):
        self.cessna172 = Plane()

    @forall(tries=50000, l=locations())
    def testFly(self, l):
        self.cessna172.fly_to(l)
        self.assertTrue(self.cessna172.has_gas())

if __name__ == '__main__':
    main()

