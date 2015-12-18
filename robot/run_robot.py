from .robot import Robot
from .robot_modules import Led, Button


class RobotRunner(object):

    """Run robot program."""

    def __init__(self):
        self.robot = Robot()
        self.robot.set_led(Led(14, 15, 18))
        self.robot.led.set_color((255, 0, 0))
        self.robot.led.on()
        self.robot.set_button(Button(23))

    def run_forever(self):
        while True:
            pass

if __name__ == "__main__":


    while True:
        if robot.button.is_pressed():
            robot.led.set_color((0, 255, 0))
            robot.led.on()
