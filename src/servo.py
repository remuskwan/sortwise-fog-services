import serial
from enum import Enum

class ServoCommand(Enum):
    Recyclable = "Recycle"
    NonRecyclable = "NonRecyclable"

SERIAL_PORT = '/dev/ttyACM0' # Hardcoded 
servo_conn = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
async def trigger_servo(command: ServoCommand):
    try:
        response = command + '\r\n'
        servo_conn.write(response)
        print(f"Response {response} successfully sent")
    except Exception as e:
        print(f"Error in trigger_servo: {e}")
