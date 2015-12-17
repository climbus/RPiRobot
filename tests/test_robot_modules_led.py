import sys, os
sys.path.append(os.path.abspath("."))

import unittest
from mock import Mock

from robot.robot_modules import Led

Led.__gpio_module__ = Mock()

class TestLed(unittest.TestCase):

    def setUp(self):
        red_pin = 1
        green_pin = 2
        blue_pin = 3
        self.led = Led(red_pin, green_pin, blue_pin)
        self.led.gpio.reset_mock()

    def test_on(self):
        self.led.on()
        self.assertEqual(self.led.red.ChangeDutyCycle.call_count, 3)
        self.assertTrue(self.led.red.called_with(self.led.reverse(self.led.color[0])))
        self.assertTrue(self.led.green.called_with(self.led.reverse(self.led.color[1])))
        self.assertTrue(self.led.blue.called_with(self.led.reverse(self.led.color[2])))

    def test_set_color(self):
        color = (1, 2, 3)
        self.led.set_color(color)
        self.assertEqual(self.led.color, color)

    def test_off(self):
        self.led.off()
        self.assertEqual(self.led.red.ChangeDutyCycle.call_count, 3)
        self.assertTrue(self.led.red.called_with(self.led.reverse(0)))

    def test_reverse(self):
        self.assertEqual(self.led.reverse(0), 255)

    def test_init(self):
        red_pin = 1
        green_pin = 2
        blue_pin = 3
        led = Led(red_pin, green_pin, blue_pin)
        self.assertEqual(led.__gpio_module__, led.gpio)

        self.assertEqual(led.red_pin, red_pin)
        self.assertEqual(led.green_pin, green_pin)
        self.assertEqual(led.blue_pin, blue_pin)

        self.assertEqual(led.gpio.PWM.call_count, 3)

        self.assertTrue(led.red.start.called)
        self.assertTrue(led.green.start.called)
        self.assertTrue(led.blue.start.called)

if __name__ == '__main__':
    unittest.main()
