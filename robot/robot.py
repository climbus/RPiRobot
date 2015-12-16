import RPi.GPIO as GPIO

class Robot(object):
    default_speed = 255;
    motors = []
    led = None
    button = None

    def set_led(self, led):
        self.led = led

    def set_motors(self, motor1, motor2):
        self.motors = [motor1, motor2]

    def set_motor(self, index, motor):
        self.motors[index] = motor

    def set_button(self, button):
        self.button = button

    def forward(self, speed=None):
        if not speed:
            speed = self.default_speed

        for m in self.motors:
            m.forward(speed)

class Led(object):

    color = (0, 0, 0)

    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        self.red = GPIO.PWM(red_pin, 100)
        self.green = GPIO.PWM(green_pin, 100)
        self.blue = GPIO.PWM(blue_pin, 100)

        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

    def set_color(color):
        self.color = color

    def on(self):
        self.red.ChangeDutyCycle(self.reverse(self.color[0]))
        self.green.ChangeDutyCycle(self.reverse(self.color[1]))
        self.blue.ChangeDutyCycle(self.reverse(self.color[2]))

    def off(self):
        self.red.ChangeDutyCycle(self.reverse(0))
        self.green.ChangeDutyCycle(self.reverse(0))
        self.blue.ChangeDutyCycle(self.reverse(0))

    def reverse(self, color):
        return 255 - color

class Motor(object):

    def __init__(self, enable_pin, input1_pin, input2_pin):
        self.enable_pin = enable_pin
        self.input1_pin = input1
        self.input2_pin = input2

        GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(input1_pin, GPIO.OUT)
        GPIO.setup(input2_pin, GPIO.OUT)

        self.enable = GPIO.PWM(enable_pin, 100)
        self.enable.start(0)


    def forward(self, speed):
        GPIO(self.input1_pin, 1)
        GPIO(self.input2_pin, 0)
        self.enable.ChangeDutyCycle(speed)

    def backward(self, speed=None):
        GPIO(self.input1_pin, 0)
        GPIO(self.input2_pin, 1)
        self.enable.ChangeDutyCycle(speed)

    def stop(self):
        self.enable.ChangeDutyCycle(0)

class Button(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def is_pressed(self):
        return GPIO.input(self.pin)


robot = Robot()
robot.set_led(Led(14, 15, 18))
robot.led.set_color((255, 0, 0))
robot.led.on()

robot.set_button(Button(23))

while True:
    if robot.button.is_pressed():
        robot.led.set_color((0, 255, 0))
        robot.led.on()

