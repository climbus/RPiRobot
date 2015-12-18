import subprocess

import RPi.GPIO as GPIO

from robot import Robot
from robot_modules import Led, Button, Motor


class RobotRunner(object):

    """Run robot program."""

    def __init__(self):
        """Set robot modules."""
        self.robot = Robot()
        self.robot.set_led(Led(14, 15, 18))
        self.robot.led.set_color((255, 0, 0))
        self.robot.led.on()
        self.robot.set_button(Button(23))
        self.robot.set_motors(Motor(25, 8, 7), Motor(16, 20, 21))

    def run_forever(self):
        """Run program in infinite loop."""
        try:
            while True:
                if self.robot.button.is_pressed():
                    self.robot.toggle_status()
                if self.robot.button.is_hold():
                    subprocess.call("halt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    RobotRunner().run_forever()
