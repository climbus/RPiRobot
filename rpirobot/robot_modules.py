import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Led(object):

    """RGB Led control module."""

    color = (0, 0, 0)
    __gpio_module__ = GPIO

    def __init__(self, red_pin, green_pin, blue_pin):
        """Module constructor."""
        self.gpio = self.__gpio_module__
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        self.gpio.setup(red_pin, self.gpio.OUT)
        self.gpio.setup(green_pin, self.gpio.OUT)
        self.gpio.setup(blue_pin, self.gpio.OUT)

        self.red = self.gpio.PWM(red_pin, 100)
        self.green = self.gpio.PWM(green_pin, 100)
        self.blue = self.gpio.PWM(blue_pin, 100)

        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

    def __del__(self):
        """Cleaning."""
        self.red.stop()
        self.green.stop()
        self.blue.stop()

    def set_color(self, color):
        """Set RGB color.

        color - tuple: (R, G, B)
        R, G, B: 0-255
        """
        self.color = color

    def on(self):
        """Turn led on."""
        self.red.ChangeDutyCycle(self.prepare_data(self.reverse(self.color[0])))
        self.green.ChangeDutyCycle(self.prepare_data(self.reverse(self.color[1])))
        self.blue.ChangeDutyCycle(self.prepare_data(self.reverse(self.color[2])))

    def off(self):
        """Turn led off."""
        self.red.ChangeDutyCycle(self.reverse(0))
        self.green.ChangeDutyCycle(self.reverse(0))
        self.blue.ChangeDutyCycle(self.reverse(0))

    @staticmethod
    def reverse(color):
        """Reverse values for katoda led type."""
        return 255 - color

    @staticmethod
    def prepare_data(val):
        """Translate 0-255 value to 0-100."""
        return round((100 * val)/255)


class Motor(object):

    """Motor module class."""

    __gpio_module__ = GPIO

    def __init__(self, enable_pin, input1_pin, input2_pin):
        """Motor constructor."""
        self.gpio = self.__gpio_module__

        self.enable_pin = enable_pin
        self.input1_pin = input1_pin
        self.input2_pin = input2_pin

        self.gpio.setup(enable_pin, self.gpio.OUT)
        self.gpio.setup(input1_pin, self.gpio.OUT)
        self.gpio.setup(input2_pin, self.gpio.OUT)

        self.enable = self.gpio.PWM(enable_pin, 100)
        self.enable.start(0)

    def forward(self, speed):
        """Run motor forward.

        speed: motor speed 0-100
        """
        if speed < 0 or speed > 100:
            raise TypeError("Speed must be between 0 and 100")

        self.gpio.output(self.input1_pin, 1)
        self.gpio.output(self.input2_pin, 0)

        self.enable.ChangeDutyCycle(speed)

    def backward(self, speed=None):
        """Move motor backward."""
        if speed < 0 or speed > 100:
            raise TypeError("Speed must be between 0 and 100")

        self.gpio.output(self.input1_pin, 0)
        self.gpio.output(self.input2_pin, 1)

        self.enable.ChangeDutyCycle(speed)

    def stop(self):
        """Stop motor."""
        self.enable.ChangeDutyCycle(0)


class Button(object):

    """Button module."""

    __gpio_module__ = GPIO
    time_set_status = None

    def __init__(self, pin):
        """Button constructor."""
        self.gpio = self.__gpio_module__
        self.pin = pin
        self.gpio.setup(pin, self.gpio.IN)
        self.status = 0

    def is_pressed(self):
        """Check if button is pressed."""
        new_status = self.gpio.input(self.pin)
        if self.status != new_status:
            self.status = new_status
            return self.status
        else:
            return 0

    def is_hold(self):
        """Check if button is holded by x seconds."""
        status = self.gpio.input(self.pin)

        if status == 1:
            if not self.time_set_status:
                self.time_set_status = time.time()
            if time.time() - self.time_set_status > 3:
                self.time_set_status = time.time()
                return 1
        else:
           self.time_set_status = None
           return 0
