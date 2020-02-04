from unittest import TestCase

from rational import rational


class TestRational(TestCase):

    def test_rational(self):
        k = rational._gcd(10, -5)
        self.assertEqual(k, 5)
        a = rational(1, 2)
        b = rational(2, 3)
        print(a + b)
        print(a - b)
        print(a * b)
        print(a / b)
        b = rational("2/3")
        print(a + b)
        print(a - b)
        print(a * b)
        print(a / b)
        self.assertEqual(a+b, "7/6")



