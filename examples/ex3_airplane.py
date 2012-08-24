class Location(object):
    def __init__(self, lat, lon, height):
        self.lat=lat
        self.lon=lon
        self.h=height
    def pr(self):
        return "LAT: " + str(self.lat) + " LON: " + str(self.lon) + " H: " + str(self.h)

class Plane(object): # class under test
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

def locations(lat = floats(-90,+90),
              lon = floats(-180, +180),
              height = floats(0, 30000)):
    while True:
        yield Location(lat.next(), lon.next(), height.next())

class TestPlane(TestCase):
    def setUp(self):
        self.cessna172 = Plane()

    @forall(tries=50000, l=locations())
    def testFly(self, l):
        self.cessna172.fly_to(l)
        self.assertTrue(self.cessna172.has_gas())

main()

