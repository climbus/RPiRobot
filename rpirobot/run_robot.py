import subprocess

import sys
print(sys.path)

import RPi.GPIO as GPIO

from rpirobot.robot import Robot
from rpirobot.robot_modules import Led, Button, Motor


class TimeoutError(Exception):

    """Exception for timeout."""

    pass


class RobotRunner(object):

    """Run robot program."""

    def __init__(self):
        """Set robot modules."""
        self.robot = create_robot()

    def run_forever(self):
        """Run program in infinite loop."""
        try:
            while True:
                if self.robot.button.is_pressed():
                    self.robot.toggle_status()
                if self.robot.button.is_hold():
                    subprocess.call("sudo shutdown -h now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except TimeoutError:
            pass
        finally:
            GPIO.cleanup()


def create_robot():
    """Robot factory."""
    robot = Robot()
    robot.set_led(Led(14, 15, 18))
    robot.led.set_color((255, 0, 0))
    robot.led.on()
    robot.set_button(Button(23))
    robot.set_motors(Motor(16, 20, 21, 1.0), Motor(25, 8, 7, 0.59))
    return robot

if __name__ == "__main__":
    RobotRunner().run_forever()
