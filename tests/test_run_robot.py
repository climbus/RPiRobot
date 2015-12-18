import sys
import os
import unittest
import time

from mock import Mock

sys.path.append(os.path.abspath("."))
from robot.run_robot import RobotRunner


from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass


class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


class TestiRunRobot(unittest.TestCase):

    """Tests for Robot class."""

    def setUp(self):
        self.robot_runner = RobotRunner()

    def test_robot_runner(self):
        self.assertIsNotNone(self.robot_runner.robot)

    def test_robot_has_led(self):
        self.assertIsNotNone(self.robot_runner.robot.led)

    def test_robot_has_button(self):
        self.assertIsNotNone(self.robot_runner.robot.button)

    def test_run_forever(self):
        tm = time.time()

        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                self.assertEqual(int(time.time() - tm), 1)

    def test_change_led_color_on_button_press(self):
        pass

if __name__ == '__main__':
    unittest.main()
