import subprocess

import RPi.GPIO as GPIO

from robot import Robot
from robot_modules import Led, Button


class RobotRunner(object):

    """Run robot program."""

    def __init__(self):
        """Set robot modules."""
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
                if self.robot.button.is_hold():
                    print("system halt")
                    subprocess.call("sudo shutdown -h now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception, e:
            print(e)
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    RobotRunner().run_forever()
