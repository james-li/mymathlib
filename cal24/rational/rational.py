#!/usr/bin/env python3

class rational:
    #def __init__(self, numerator:int, denominator = 1):
    def __init__(self, *args, **kwargs):
        numerator = args[0]
        denominator = 1
        if type(numerator) == int:
            if len(args) > 1:
                denominator = args[1]
        elif type(numerator) == str:
            nl = numerator.split('/')
            if len(nl) == 1:
                numerator = int(nl[0])
                denominator = 1
            elif len(nl) == 2:
                numerator = int(nl[0])
                denominator = int(nl[1])
            else:
                raise SyntaxError("Invalid data format")
        else:
            raise SyntaxError("Invalid data format")

        g = rational._gcd(numerator, denominator)
        self._numerator = int(numerator / g)
        self._denominator = int(denominator /g)
        if self._denominator < 0:
            self._numerator = - self._numerator
            self._denominator = - self._denominator

    @staticmethod
    def _gcd(a, b):
        if b == 0:
            return a if a > 0 else -a
        else:
            return rational._gcd(b, a % b)

    def __add__(self, *args):
        v = args[0]
        if type(v) != rational:
            v = rational(v)
        n =self._numerator * v._denominator + self._denominator * v._numerator
        d = self._denominator * v._denominator
        return rational(n, d)


    def __sub__(self, *args):
        v = args[0]
        if type(v) != rational:
            v = rational(v)
        n =self._numerator * v._denominator - self._denominator * v._numerator
        d = self._denominator * v._denominator
        return rational(n, d)

    def __mul__(self, *args):
        v = args[0]
        if type(v) != rational:
            v = rational(v)
        n = self._numerator * v._numerator
        d = self._denominator * v._denominator
        return rational(n, d)

    def __truediv__(self, *args):
        v = args[0]
        if type(v) != rational:
            v = rational(v)
        n = self._numerator * v._denominator
        d = self._denominator * v._numerator
        return rational(n, d)

    def __eq__(self, *args):
        v = args[0]
        if type(v) == rational:
            return self._numerator * v._denominator == self._denominator * v._numerator
        else:
            try:
                return self.__eq__(rational(v))
            except:
                return False

    def int_value(self):
        return int(self._numerator/self._denominator)

    def __repr__(self):
        if self._denominator == 1:
            return str(self._numerator)
        else:
            return "%d/%d"%(self._numerator, self._denominator)