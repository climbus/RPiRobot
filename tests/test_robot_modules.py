import sys
import os
import unittest

sys.path.append(os.path.abspath("."))


class TestRobotModules(unittest.TestCase):

    """Tests for robot modules file."""

    def test_gpio(self):
        try:
            from robot.robot_modules import GPIO
        except ImportError:
            self.fail("GPIO not found")

        try:
            GPIO()
        except:
            pass

if __name__ == '__main__':
    unittest.main()
