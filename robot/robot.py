from .modules import Led, Button


class Robot(object):

    """Robot class."""

    default_speed = 255
    motors = []
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

robot = Robot()
robot.set_led(Led(14, 15, 18))
robot.led.set_color((255, 0, 0))
robot.led.on()

robot.set_button(Button(23))

while True:
    if robot.button.is_pressed():
        robot.led.set_color((0, 255, 0))
        robot.led.on()
