import sys
import os
import unittest
import time

from mock import Mock, patch

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
        self.robot.change_status = Mock()
        self.robot._stop_motors = Mock()
        self._set_motors()
        self.robot.forward()
        self.assertTrue(self.robot._stop_motors.called)
        self.assertTrue(self.robot.motors[0].forward.called)
        self.assertTrue(self.robot.motors[1].forward.called)

    def test_forward_default_speed(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.forward()
        self.robot.motors[0].forward.called_with(self.robot.default_speed)
        self.robot.motors[1].forward.called_with(self.robot.default_speed)

    def test_forward_with_speed(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.forward(speed=50)
        self.robot.motors[0].forward.called_with(50)
        self.robot.motors[1].forward.called_with(self.robot.default_speed)

    def test_robot_has_status(self):
        self.assertIsNotNone(self.robot.status)

    def test_robot_starts_with_status(self):
        self.assertEqual(self.robot.status, -1)

    def test_robot_colud_change_status(self):
        self._set_motors()
        self.robot.set_led(Mock())
        self.robot.change_status(1)
        self.assertEqual(self.robot.status, 1)

    def test_led_changes_color_after_status_change(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.change_status(1)
        self.assertTrue(self.robot.led.set_color.called)
        self.assertTrue(self.robot.led.on.called)

    def test_should_stop_on_status_minus_1(self):
        self.robot.set_led(Mock())
        self.robot._stop_motors = Mock()
        self._set_motors()
        self.robot.change_status(-1)
        self.assertTrue(self.robot._stop_motors.called)

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
        self.robot._stop_motors = Mock()
        self.robot.stop()
        self.assertTrue(self.robot._stop_motors.called)

    def test_left(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot._stop_motors = Mock()
        self.robot.left()
        self.assertTrue(self.robot._stop_motors.called)
        self.assertEqual(self.robot.motors[0].forward.call_count, 1)
        self.assertEqual(self.robot.motors[1].forward.call_count, 0)

    def test_right(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot._stop_motors = Mock()
        self.robot.right()
        self.assertTrue(self.robot._stop_motors.called)
        self.assertEqual(self.robot.motors[1].forward.call_count, 1)
        self.assertEqual(self.robot.motors[0].forward.call_count, 0)

    def test_left_default_speed(self):
        self._set_motors()
        self.robot.left()
        self.robot.motors[0].forward.assert_called_with(self.robot.default_speed)

    def test_left_with_speed(self):
        self._set_motors()
        self.robot.left(speed=50)
        self.robot.motors[0].forward.assert_called_with(50)

    def test_left_with_angle(self):
        self._set_motors()
        self.robot.stop = Mock()
        self.robot.width = 13
        self.robot.cps = 10
        tm = time.time()
        self.robot.left(angle=90)
        self.assertEqual(round(time.time() - tm), 2)

    def test_left_first_param_angle(self):
        self._set_motors()
        self.robot._go_for_distance = Mock()
        self.robot.width = 13
        self.robot.cps = 10
        self.robot.left(50)
        self.assertEqual(round(self.robot._go_for_distance.call_args[0][0]), 11)

    def test_right_with_angle(self):
        self._set_motors()
        self.robot.stop = Mock()
        self.robot.width = 13
        self.robot.cps = 10
        tm = time.time()
        self.robot.right(angle=90)
        self.assertEqual(round(time.time() - tm), 2)

    def test_right_default_speed(self):
        self._set_motors()
        self.robot.right()
        self.robot.motors[1].forward.assert_called_with(self.robot.default_speed)

    def test_right_with_speed(self):
        self._set_motors()
        self.robot.right(speed=50)
        self.robot.motors[1].forward.assert_called_with(50)

    def test_right_first_param_angle(self):
        self._set_motors()
        self.robot._go_for_distance = Mock()
        self.robot.width = 13
        self.robot.cps = 10
        self.robot.right(50)
        self.assertEqual(round(self.robot._go_for_distance.call_args[0][0]), 11)

    def test_forward_with_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.cps = 10
        tm = time.time()
        self.robot.forward(distance=10)
        self.assertEqual(round(time.time() - tm), 1)

    def test_forward_with_small_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.cps = 10
        tm = time.time()
        self.robot.forward(distance=5)
        self.assertEqual(round(time.time() - tm, 1), 0.5)

    def test_forward_first_param_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot._go_for_distance = Mock()
        self.robot.forward(50)
        self.robot._go_for_distance.assert_called_with(50)

    def test_back(self):
        self._set_motors()
        self.robot._stop_motors = Mock()
        self.robot.back()
        self.assertTrue(self.robot._stop_motors.called)
        self.assertTrue(self.robot.motors[0].backward.called)
        self.assertTrue(self.robot.motors[1].backward.called)

    def test_back_default_speed(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.back()
        self.robot.motors[0].backward.assert_called_with(self.robot.default_speed)
        self.robot.motors[1].backward.assert_called_with(self.robot.default_speed)

    def test_back_with_speed(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.back(speed=50)
        self.robot.motors[0].backward.assert_called_with(50)
        self.robot.motors[1].backward.assert_called_with(50)

    def test_back_with_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.cps = 10
        tm = time.time()
        self.robot.back(distance=10)
        self.assertEqual(round(time.time() - tm), 1)

    def test_back_first_param_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot._go_for_distance = Mock()
        self.robot.back(50)
        self.robot._go_for_distance.assert_called_with(50)


    def test_back_with_small_distance(self):
        self.robot.change_status = Mock()
        self._set_motors()
        self.robot.cps = 10
        tm = time.time()
        self.robot.back(distance=5)
        self.assertEqual(round(time.time() - tm, 1), 0.5)

    def test_get_speed(self):
        self.robot.default_speed = 10
        self.assertEqual(self.robot._get_speed(20), 20)

    def test_get_speed_none(self):
        self.robot.default_speed = 10
        self.assertEqual(self.robot._get_speed(None), 10)

    @patch("rpirobot.robot.time")
    def test_go_for_distance(self, time):
        self.robot.set_led(Mock())
        self._set_motors()
        distance = 10
        self.robot.cps = 10
        self.robot._go_for_distance(10)
        time.sleep.assert_called_with(1)

    @patch("rpirobot.robot.time")
    def test_dont_go_if_distance_none(self, time):
        self.robot._go_for_distance(None)
        self.assertFalse(time.sleep.called)

    def test_angle_to_distance(self):
        self.robot.width = 10
        self.assertEqual(round(self.robot._angle_to_distance(90)), 16)

    def test_angle_to_distance_none(self):
        self.assertIsNone(self.robot._angle_to_distance(None))

    def test_stop_changes_status(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.status = None
        self.robot.stop()
        self.assertEqual(self.robot.status, 0)

    def test_forward_changes_status(self):
        self.robot.set_led(Mock())
        self._set_motors()
        self.robot.status = None
        self.robot.forward()
        self.assertEqual(self.robot.status, 1)

    def test_stop_motors(self):
        self._set_motors()
        self.robot._stop_motors()
        self.assertTrue(self.robot.motors[0].stop.called)
        self.assertTrue(self.robot.motors[1].stop.called)

    def _set_motors(self):
        self.robot.set_motors(Mock(), Mock())

if __name__ == '__main__':
    unittest.main()
