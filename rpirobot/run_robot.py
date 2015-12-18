import RPi.GPIO as GPIO

from robot import Robot
from robot_modules import Led, Button


class RobotRunner(object):

    """Run robot program."""

    def __init__(self):
        """Sets robot modules."""
        self.robot = Robot()
        self.robot.set_led(Led(14, 15, 18))
        self.robot.led.set_color((255, 0, 0))
        self.robot.led.on()
        self.robot.set_button(Button(23))

    def run_forever(self):
        """Run program in infinite loop."""
        try:
            while True:
                if self.robot.button.is_pressed():
                    self.robot.toggle_status()
        except:
            pass
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    RobotRunner().run_forever()
