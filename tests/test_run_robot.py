import sys
import os
import unittest
import time
import signal

from mock import Mock, patch

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("rpirobot"))
from rpirobot.run_robot import RobotRunner


class TimeoutError(Exception):
    pass


class timeout(object):

    """Timeout util."""

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
    @patch('rpirobot.run_robot.Motor')
    def setUp(self, Led, Button, Robot, Motor):
        self.robot_runner = RobotRunner()

    def test_robot_runner(self):
        self.assertIsNotNone(self.robot_runner.robot)

    def test_robot_sets_led(self):
        self.assertTrue(self.robot_runner.robot.set_led.called)

    def test_robot_sets_button(self):
        self.assertTrue(self.robot_runner.robot.set_button.called)

    def test_robot_sets_motors(self):
        self.assertTrue(self.robot_runner.robot.set_motors.called)

    def test_run_forever(self):
        self.robot_runner.robot.button.is_hold = Mock(return_value=0)
        tm = time.time()

        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertEqual(int(time.time() - tm), 1)

    def test_toggle_status_on_button_press(self):
        self.robot_runner.robot.button.is_pressed = Mock(return_value=1)
        self.robot_runner.robot.button.is_hold = Mock(return_value=0)

        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertTrue(self.robot_runner.robot.toggle_status.called)

    def test_check_if_button_pressed(self):
        self.robot_runner.robot.button.reset_mock()
        self.robot_runner.robot.button.is_hold = Mock(return_value=0)
        with timeout(seconds=1):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertTrue(self.robot_runner.robot.button.is_pressed.called)

    @patch('rpirobot.run_robot.subprocess')
    def test_system_halt_on_button_hold(self, subprocess):
        self.robot_runner.robot.button.is_hold = Mock(return_value=1)

        with timeout(seconds=4):
            try:
                self.robot_runner.run_forever()
            except TimeoutError:
                pass
        self.assertTrue(subprocess.call.called)

if __name__ == '__main__':
    unittest.main()
