import status
from datetime import date
from tornado import web, escape, ioloop, httpclient, gen
from drone import Altimeter, Drone, Hexacopter, LightEmittingDiode


drone = Drone()


class HexacopterHandler(web.RequestHandler):
    SUPPORT_METHODS = ("GET", "PATCH")
    HEXACOPTER_ID = 1

    def get(self, id):
        if int(id) is not self.HEXACOPTER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        print("I've started retrieving hexacopter's status")
        hexacopter_status = drone.hexacopeter.get_hexacopter_status()
        print("I've finished retrieving hexacopter's status")
        response = {
            "speed": hexacopter_status.motor_speed,
            "turned_on": hexacopter_status.turned_on,
        }
        self.set_status(status.HTTP_200_OK)
        self.write(response)

    def patch(self, id):
        if int(id) is not self.HEXACOPTER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        request_data = escape.json_decode(self.request.body)
        if (
            "motor_speed" not in request_data.keys() or
            request_data["motor_speed"] is None
        ):
            self.set_status(status.HTTP_400_BAD_REQUEST)
            return
        try:
            motor_speed = int(request_data["motor_speed"])
            print("I've started setting the hexacopter's motor speed")
            hexacopter_status = drone.hexacopeter.set_motor_speed(motor_speed)
            print("I've finished setting the hexacopet's motor speed")
            response = {
                "speed": hexacopter_status.motor_speed,
                "turned_on": hexacopter_status.turned_on,
            }
            self.set_status(status.HTTP_200_OK)
            self.write(response)
        except ValueError as e:
            print("I've failed setting the hexacopter's motor speed")
            self.set_status(status.HTTP_400_BAD_REQUEST)
            response = {
                "error": e.args[0]
            }
            self.write(response)


class LedHandler(web.RequestHandler):
    SUPPORT_METHODS = ("GET", "PATCH")

    def get(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        led = drone.leds[int_id]
        print(f"I've started retrieving {led.description} status")
        brightness_level = led.get_brightness_level()
        print(f"I've finished retrieving {led.description} status")
        response = {
            "id": led.identifier,
            "description": led.description,
            "brightness_level": brightness_level,
        }
        self.set_status(status.HTTP_200_OK)
        self.write(response)

    def patch(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        request_data = escape.json_decode(self.request.body)
        if (
            "brightness_level" not in request_data.keys() or
            request_data["brightness_level"] is None
        ):
            self.set_status(status.HTTP_400_BAD_REQUEST)
            return
        led = drone.leds[int_id]
        try:
            brightness_level = int(request_data["brightness_level"])
            print(f"I've started setting the {led.description} motor speed")
            led.set_brightness_level(brightness_level)
            print(f"I've finished setting the {led.description}  motor speed")
            response = {
                "id": led.identifier,
                "description": led.description,
                "brightness_level": brightness_level,
            }
            self.set_status(status.HTTP_200_OK)
            self.write(response)
        except ValueError as e:
            print(f"I've failed setting the {led.description} motor speed")
            self.set_status(status.HTTP_400_BAD_REQUEST)
            response = {
                "error": e.args[0]
            }
            self.write(response)


class AltimeterHandler(web.RequestHandler):
    SUPPORT_METHODS = "GET"
    ALTIMETER_ID = 1

    def get(self, id):
        if int(id) is not self.ALTIMETER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        print("I've started retrieving the altitude")
        altitude = drone.get_alitude()
        print("I've finished retrieving the altitude")
        response = {
            "altitude": altitude
        }
        self.set_status(status.HTTP_200_OK)
        self.set_status(status.HTTP_200_OK)
        self.write(response)


application = web.Application([
    (r"/hexacopters/([0-9]+)", HexacopterHandler),
    (r"/leds/([0-9]+)", LedHandler),
    (r"/altimeters/([0-9]+)", AltimeterHandler),
], debug=True)

if __name__ == "__main__":
    port = 8888
    print(f"Listening at port {port}")
    application.listen(port)
    ioloop.IOLoop.instance().start()