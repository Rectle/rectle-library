import unittest

from log import log


class LogTest(unittest.TestCase):

    def test_exist(self):
        try:
            log()
        except Exception:
            self.fail()

if __name__ == '__main__':
    unittest.main()
