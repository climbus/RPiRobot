import sys
import os
import unittest
from mock import Mock

sys.path.append(os.path.abspath("."))
from robot.robot_modules import Motor

Motor.__gpio_module__ = Mock()


class TestMotor(unittest.TestCase):

    """Tests for class Motor."""

    def setUp(self):
        self.enable_pin = 1
        self.input1_pin = 2
        self.input2_pin = 3

        Motor.__gpio_module__.reset_mock()
        self.motor = Motor(self.enable_pin, self.input1_pin, self.input2_pin)

    def test_init(self):
        self.assertEqual(self.motor.__gpio_module__, self.motor.gpio)
        self.assertEqual(self.motor.enable_pin, self.enable_pin)
        self.assertEqual(self.motor.input1_pin, self.input1_pin)
        self.assertEqual(self.motor.input2_pin, self.input2_pin)

        self.assertEqual(self.motor.gpio.setup.call_count, 3)
        self.assertTrue(self.motor.gpio.PWM.called)
        self.assertTrue(self.motor.enable.start.called)

    def test_forward(self):
        self.motor.forward(100)
        self.motor.gpio.output.assert_any_call(self.input1_pin, 1)
        self.motor.gpio.output.assert_any_call(self.input2_pin, 0)
        self.assertTrue(self.motor.enable.ChangeDutyCycle.called)

    def test_forward_without_speed(self):
        with self.assertRaises(TypeError):
            self.motor.forward()

    def test_forward_max_speed(self):
        self.motor.forward(100)
        self.motor.enable.ChangeDutyCycle.assert_called_with(100)

    def test_forward_min_speed(self):
        self.motor.forward(0)
        self.motor.enable.ChangeDutyCycle.assert_called_with(0)

    def test_forward_speed_out_of_bounds(self):
        speeds = (-1, 200, 101)
        for speed in speeds:
            with self.assertRaises(TypeError):
                self.motor.forward(speed)

    def test_backward(self):
        self.motor.backward(100)
        self.motor.gpio.output.assert_any_call(self.input1_pin, 0)
        self.motor.gpio.output.assert_any_call(self.input2_pin, 1)
        self.assertTrue(self.motor.enable.ChangeDutyCycle.called)

    def test_backward_without_speed(self):
        with self.assertRaises(TypeError):
            self.motor.backward()

    def test_backward_max_speed(self):
        self.motor.backward(100)
        self.motor.enable.ChangeDutyCycle.assert_called_with(100)

    def test_backward_min_speed(self):
        self.motor.backward(0)
        self.motor.enable.ChangeDutyCycle.assert_called_with(0)

    def test_backward_speed_out_of_bounds(self):
        speeds = (-1, 200, 101)
        for speed in speeds:
            with self.assertRaises(TypeError):
                self.motor.backward(speed)

    def test_stop(self):
        self.motor.stop()
        self.motor.enable.ChangeDutyCycle.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()
