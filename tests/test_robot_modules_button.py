import sys
import os
import time

sys.path.append(os.path.abspath("."))

import unittest
from mock import Mock, MagicMock

from rpirobot.robot_modules import Button

Button.__gpio_module__ = Mock()

class TestButton(unittest.TestCase):

    def setUp(self):
        self.pin = 1
        self.btn = Button(self.pin)
        self.btn.gpio.reset_mock()

    def test_init(self):
        self.assertEqual(self.btn.__gpio_module__, self.btn.gpio)
        self.assertEqual(self.btn.pin, self.pin)

    def test_is_pressed_calls_gpio(self):
        self.btn.gpio.input = MagicMock(return_value=1)
        self.btn.is_pressed()
        self.btn.gpio.input.assert_called_with(self.pin)

    def test_is_pressed_true(self):
        self.btn.gpio.input = MagicMock(return_value=1)

        return_val = self.btn.is_pressed()

        self.assertEqual(return_val, 1)

    def test_is_pressed_false(self):
        self.btn.gpio.input = MagicMock(return_value=0)

        return_val = self.btn.is_pressed()

        self.assertEqual(return_val, 0)

    def test_continous_button_press_trigger_only_once(self):
        self.btn.gpio.input = MagicMock(return_value=1)

        vals = []
        for i in range(10):
            vals.append(self.btn.is_pressed())

        self.assertEqual(len([v for v in vals if v == 1]), 1)

    def test_is_button_hlod(self):
        self.btn.gpio.input = MagicMock(return_value=1)
        tm = time.time()
        while time.time() - tm < 4:
            val = self.btn.is_hold()
            if val == 1:
                break
        self.assertEqual(val, 1)

    def test_is_not_hold(self):
        self.btn.gpio.input = MagicMock(return_value=0)
        tm = time.time()
        while time.time() - tm < 4:
            val = self.btn.is_hold()
            if val == 1:
                break
        self.assertEqual(val, 0)

if __name__ == '__main__':
    unittest.main()
