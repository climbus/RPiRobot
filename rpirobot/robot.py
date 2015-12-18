

class Robot(object):

    """Robot class."""

    default_speed = 255
    motors = [None, None]
    led = None
    button = None
    status = -1
    colors = {-1: (255, 0, 0), 1: (0, 255, 0), 0: (0, 255, 0)}

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

    def change_status(self, status):
        """Change status."""
        self.led.set_color(self.colors[status])
        self.led.on()
        self.status = status

    def toggle_status(self):
        """Toggle status: on(0), off(-1)."""
        if self.status == -1:
            self.change_status(0)
        else:
            self.change_status(-1)
