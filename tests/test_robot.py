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

    def test_robot_has_status(self):
        self.assertIsNotNone(self.robot.status)

    def test_robot_starts_with_status(self):
        self.assertEqual(self.robot.status, -1)

    def test_robot_colud_change_status(self):
        self._set_motors()
        self.robot.set_led(Mock())
        self.robot.change_status(1)
        self.assertEqual(self.robot.status, 1)

    def test_led_changes_color_after_status_chanhe(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.change_status(1)
        self.assertTrue(self.robot.led.set_color.called)
        self.assertTrue(self.robot.led.on.called)

    def test_sholud_run_motors_on_status_1(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.change_status(1)
        self.assertTrue(self.robot.motors[0].forward.called)
        self.assertTrue(self.robot.motors[1].forward.called)

    def test_should_stop_on_status_minus_1(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.change_status(-1)
        self.assertTrue(self.robot.motors[0].stop.called)
        self.assertTrue(self.robot.motors[1].stop.called)

    def test_could_toggle_status(self):
        self._set_motors()
        self.robot.set_led(Mock())
        self.robot.status = -1
        self.robot.toggle_status()
        self.assertEqual(self.robot.status, 1)
        self.robot.toggle_status()
        self.assertEqual(self.robot.status, -1)

    def test_stop(self):
        self._set_motors()
        self.robot.set_led(Mock())
        self.robot.stop()
        self.assertEqual(self.motor.stop.call_count, 2)

    def test_left(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.stop = Mock()
        self.robot.left()
        self.assertEqual(self.robot.stop.call_count, 1)
        self.assertEqual(self.motor.forward.call_count, 1)

    def _set_motors(self):
        self. motor = Mock()
        self.robot.set_motors(self.motor, self.motor)

if __name__ == '__main__':
    unittest.main()
