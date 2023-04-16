class IdentifiedObject:

    def __init__(self, oid):
        self._oid = oid  # read only PROPERTY - means you can access it without the method call.

        #  difference between one + two underscores - _this means protected. __this IS enforced by python.
        #  you tend to use single underscores - ideally make it as simple as needed.

    @property   # it allows some other class to modify your class at compile time. so other.oid AND other.oid() work
    def oid(self):
        return self._oid

    def __eq__(self, other):
        return type(self) == type(other) and self._oid == other.oid  # this still calls the getter ANYWAY.

    def __hash__(self):
        return hash(self._oid)
