from .robot_modules import Led, Button


class Robot(object):

    """Robot class."""

    default_speed = 255
    motors = [None, None]
    led = None
    button = None

    def set_led(self, led):
        """Set led object."""
        self.led = led

    def set_motors(self, motor1, motor2):
        """Set motors objects."""
        self.motors = [motor1, motor2]

    def set_motor(self, index, motor):
        """Set one motor on given index."""
        self.motors[index] = motor

    def set_button(self, button):
        """Set button object."""
        self.button = button

    def forward(self, speed=None):
        """Move robot forward."""
        if not speed:
            speed = self.default_speed

        for m in self.motors:
            m.forward(speed)
