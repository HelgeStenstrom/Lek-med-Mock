import unittest
from unittest.mock import MagicMock


class A:
    def __init__(self):
        self.count = 0
        self.ignored = None

    def do_stuff(self, arg):
        raise Exception  # abstract function

    def update(self, ignore):
        self.count += 1
        self.ignored = ignore


class B(A):
    def __init__(self):
        super().__init__()
        self.args = []

    def do_stuff(self, arg):
        self.args += [arg]
        self.update(arg)

# Unit tests


class SomeTests(unittest.TestCase):
    def setUp(self):
        self.b = B()
        pass

    def tearDown(self):
        pass

    def qtest_that_fails(self):
        self.fail("för att ett test ska faila.")

    def test_that_args_are_collected(self):

        self.b.do_stuff("ett")
        self.b.do_stuff("två")
        self.assertEqual(self.b.args, ["ett", "två"])

    def test_that_calls_are_counted(self):
        [self.b.do_stuff(n) for n in range(17)]
        self.assertEqual(self.b.count, 17)

    def test_that_update_is_called(self):
        update = MagicMock()
        self.b.update = update

        self.b.do_stuff(4711)

        update.assert_called_with(4711)
        update.assert_called_with(4711)
        self.b.update.assert_called_with(4711)
        # Det går bra att anropa samma assert flera gånger.
        # PyCharm förstår att update har metoden assert_called_with,
        # men inte att self.b.update har det. Därför tricket att self.b.update = mm.
