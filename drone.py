from random import randint
from time import sleep


class HexacopterStatus:
    def __init__(self, motor_speed, turned_on):
        self.motor_speed = motor_speed
        self.turned_on = turned_on


class Hexacopter:
    MIN_SPEED = 0
    MAX_SPEED = 1000

    def __init__(self):
        self.motor_speed = self.MIN_SPEED
        self.turned_on = False

    def get_motor_speed(self):
        return self.motor_speed

    def set_motor_speed(self, motor_speed):
        if motor_speed < self.MIN_SPEED:
            raise ValueError(f"The minimum speed is {self.MIN_SPEED}")
        if motor_speed > self.MAX_SPEED:
            raise ValueError(f"The maximum speed is {self.MAX_SPEED}")
        self.motor_speed = motor_speed
        self.turned_on = self.motor_speed != 0
        sleep(2)
        return HexacopterStatus(self.get_motor_speed(), self.is_turned_on())

    def is_turned_on(self):
        return self.turned_on

    def get_hexacopter_status(self):
        sleep(3)
        return HexacopterStatus(self.get_motor_speed(), self.is_turned_on())


class LightEmittingDiode:
    MIN_BRIGHTNESS_LEVEL = 0
    MAX_BRIGHTNESS_LEVEL = 255

    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description
        self.brightness_level = self.MIN_BRIGHTNESS_LEVEL

    def get_brightness_level(self):
        sleep(1)
        return self.brightness_level

    def set_brightness_level(self, brightness_level):
        if brightness_level < self.MIN_BRIGHTNESS_LEVEL:
            raise ValueError(f"The minimum brightness level is {self.MIN_BRIGHTNESS_LEVEL}")
        if brightness_level > self.MAX_BRIGHTNESS_LEVEL:
            raise ValueError(f"The maximum brightness level is {self.MAX_BRIGHTNESS_LEVEL}")
        sleep(2)
        self.brightness_level = brightness_level


class Altimeter:
    def get_altimeter(self):
        sleep(1)
        return randint(0, 3000)


class Drone:
    def __init__(self):
        self.hexacopeter = Hexacopter()
        self.altimeter = Altimeter()
        self.blue_led = LightEmittingDiode(1, "Blue LED")
        self.white_led = LightEmittingDiode(2, "White LED")
        self.leds = {
            self.blue_led.identifier: self.blue_led,
            self.white_led.identifier: self.white_led,
        }
