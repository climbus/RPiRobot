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

    def forward(self, distance=None, speed=None):
        """Move robot forward."""
        speed = self._get_speed(speed)

        for m in self.motors:
            m.forward(speed)

        self._go_for_distance(distance)

    def back(self, distance=None, speed=None):
        """Move robot backward."""
        speed = self._get_speed(speed)

        for m in self.motors:
            m.backward(speed)

        self._go_for_distance(distance)

    def stop(self):
        """Stop robot."""
        for m in self.motors:
            m.stop()

    def left(self, angle=None, speed=None):
        """Turn robot left."""
        speed = self._get_speed(speed)

        self.stop()
        self.motors[0].forward(speed)

        self._go_for_distance(self._angle_to_distance(angle))

    def right(self, angle=None, speed=None):
        """Turn robot left."""
        speed = self._get_speed(speed)

        self.stop()
        self.motors[1].forward(speed)

        self._go_for_distance(self._angle_to_distance(angle))

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

    def _get_speed(self, speed):
        """Set speed to default if None."""
        if not speed:
            return self.default_speed
        else:
            return speed

    def _go_for_distance(self, distance):
        if distance is None:
            return
        go_time = float(distance) / float(self.cps)
        time.sleep(go_time)
        self.stop()

    def _angle_to_distance(self, angle):
        if angle is None:
            return angle
        else:
            return (float(self.width)*math.pi * 2) * (float(angle)/360)
