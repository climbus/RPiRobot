import time
import math


class Robot(object):

    """Robot class."""

    default_speed = 100
    motors = [None, None]
    led = None
    button = None
    status = -1
    colors = {-1: (255, 0, 0), 1: (0, 255, 0), 0: (0, 255, 0)}

    cps = 35
    width = 15

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

    def forward(self, speed=None, distance=None):
        """Move robot forward."""
        if not speed:
            speed = self.default_speed

        for m in self.motors:
            m.forward(speed)

        if distance is not None:
            time.sleep(float(distance) / float(self.cps))
            self.stop()

    def stop(self):
        """Stop robot."""
        for m in self.motors:
            m.stop()

    def left(self, speed=None, angle=None):
        """Turn robot left."""
        if not speed:
            speed = self.default_speed

        self.stop()
        self.motors[0].forward(speed)

        if angle is not None:
            time.sleep(((float(self.width)*math.pi) * (float(angle)/360)) / float(self.cps) * 2)
            self.motors[0].stop()

    def right(self, speed=None, angle=None):
        """Turn robot left."""
        if not speed:
            speed = self.default_speed

        self.stop()
        self.motors[1].forward(speed)

        if angle is not None:
            time.sleep(((float(self.width)*math.pi) * (float(angle)/360)) / float(self.cps) * 2)
            self.motors[1].stop()

    def change_status(self, status):
        """Change status."""
        self.led.set_color(self.colors[status])
        self.led.on()
        self.status = status
        if status == 1:
            self.forward()
        if status == -1:
            self.stop()

    def toggle_status(self):
        """Toggle status: on(0), off(-1)."""
        if self.status == -1:
            self.change_status(1)
        else:
            self.change_status(-1)
