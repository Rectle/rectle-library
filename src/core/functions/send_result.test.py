import unittest

from send_result import send_result, _prepare_arguments


class SendResultTest(unittest.TestCase):

    def test_exist(self):
        try:
            send_result()
        except Exception:
            self.fail()

    def test_positional_arguments(self):
        args = _prepare_arguments(100)
        self.assertEqual(args, {"arg0": 100})

        args = _prepare_arguments(100, 50.3, True)
        self.assertEqual(args, {"arg0": 100, "arg1": 50.3, "arg2": True})

        args = _prepare_arguments(0x64, -.3, "ok")
        self.assertEqual(args, {"arg0": 0x64, "arg1": -.3, "arg2": "ok"})

    def test_keyword_arguments(self):
        args = _prepare_arguments(points=100, time=10)
        self.assertEqual(args, {"points": 100, "time": 10})
        
        args = _prepare_arguments(points=100, time=0.95, passed=True, result="ok")
        self.assertEqual(args, {"points": 100, "time": 0.95, "passed": True, "result": "ok"})

    def test_mixed_arguments(self):
        args = _prepare_arguments(100, time=15)
        self.assertEqual(args, {"arg0": 100, "time": 15})
        
        args = _prepare_arguments(100, arg0=0, time=15)
        self.assertEqual(args, {"arg0": 0, "arg1": 100, "time": 15})
        
        args = _prepare_arguments(100, True, arg1="ok", points=123, time=15)
        self.assertEqual(args, {"arg0": 100, "arg1": "ok", "arg2": True, "points": 123, "time": 15})

if __name__ == '__main__':
    unittest.main()
