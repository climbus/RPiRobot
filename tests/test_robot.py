import sys
import os
import unittest
from mock import Mock

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("rpirobot"))
from rpirobot.robot import Robot

class TestRobot(unittest.TestCase):

    """Tests for Robot class."""

    def setUp(self):
        self.robot = Robot()

    def test_set_led(self):
        led = Mock()
        self.robot.set_led(led)
        self.assertEqual(self.robot.led, led)

    def test_set_motors(self):
        motor1 = Mock()
        motor2 = Mock()
        self.robot.set_motors(motor1,  motor2)
        self.assertEqual(self.robot.motors[0], motor1)
        self.assertEqual(self.robot.motors[1], motor2)

    def test_set_motor(self):
        motor = Mock()
        index = 1
        self.robot.set_motor(index, motor)
        self.assertEqual(self.robot.motors[1], motor)

    def test_set_motor_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.robot.set_motor(2, None)

    def test_set_button(self):
        button = Mock()
        self.robot.set_button(button)
        self.assertEqual(self.robot.button, button)

    def test_forward(self):
        self._set_motors()
        self.robot.forward()
        self.assertEqual(self.motor.forward.call_count, 2)

    def test_forward_default_speed(self):
        self._set_motors()
        self.robot.forward()
        self.motor.forward.called_with(self.robot.default_speed)

    def test_forward_with_speed(self):
        self._set_motors()
        self.robot.forward(50)
        self.motor.forward.called_with(50)

    def _set_motors(self):
        self. motor = Mock()
        self.robot.set_motors(self.motor, self.motor)

if __name__ == '__main__':
    unittest.main()
