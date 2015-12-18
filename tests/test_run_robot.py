import sys
import os
import unittest
import time

from mock import Mock, patch

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("rpirobot"))
from rpirobot.run_robot import RobotRunner


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

    @patch('rpirobot.run_robot.Led')
    @patch('rpirobot.run_robot.Button')
    @patch('rpirobot.run_robot.Robot')
    def setUp(self, Led, Button, Robot):
        self.robot_runner = RobotRunner()

    def test_robot_runner(self):
        self.assertIsNotNone(self.robot_runner.robot)

    def test_robot_sets_led(self):
        self.assertTrue(self.robot_runner.robot.set_led.called)

    def test_robot_sets_button(self):
        self.assertTrue(self.robot_runner.robot.set_button.called)

    def test_run_forever(self):
        tm = time.time()

        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertEqual(int(time.time() - tm), 1)

    def test_change_led_color_on_button_press(self):
        self.robot_runner.robot.led.reset_mock()
        self.robot_runner.robot.button.is_pressed = Mock(return_value=1)

        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertTrue(self.robot_runner.robot.led.set_color.called)
        self.assertTrue(self.robot_runner.robot.led.on.called)

    def test_check_if_button_pressed(self):
        self.robot_runner.robot.button.reset_mock()
        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertTrue(self.robot_runner.robot.button.is_pressed.called)


if __name__ == '__main__':
    unittest.main()
