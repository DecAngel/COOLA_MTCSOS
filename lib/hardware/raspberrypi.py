import board
import adafruit_dht
import seeed_sgp30
from grove.i2c import Bus

dhtDevice = None
sgp30 = None

def init():
    dhtDevice = adafruit_dht.DHT22(board.D26, use_pulseio=False)
    sgp30=seeed_sgp30.grove_sgp30(Bus())

def action(action,args):
    pass

def get_sensor_list():
    return {
        'sgp30':0,
        'dht22':1
    }


def get_sensor(sensor_id):
    if sensor_id == 0:
        return read_sensor_sgp30()
    if sensor_id == 1:
        return read_sensor_dht22()


def read_sensor_dht22():
    try:
        temperature_c=dhtDevice.temperature
        humidity=dhtDevice.humidity
        return {
            'temperature_c':temperature_c,
            'humidity':humidity
        }
    except RuntimeError as _:
        return None

def read_sensor_sgp30():
    co2_eq_ppm, tvoc_ppb = sgp30.read_measurements().data
    return {
        'co2_eq_ppm':co2_eq_ppm,
        'tvoc_ppb':tvoc_ppb
    }

