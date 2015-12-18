
robot = Robot()
robot.set_led(Led(14, 15, 18))
robot.led.set_color((255, 0, 0))
robot.led.on()

robot.set_button(Button(23))

while True:
    if robot.button.is_pressed():
        robot.led.set_color((0, 255, 0))
        robot.led.on()
