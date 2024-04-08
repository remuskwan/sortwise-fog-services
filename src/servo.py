import serial
from enum import Enum
from fastapi import APIRouter

class ServoCommand(Enum):
    def __str__(self) -> str:
        return str(self.value)
    Recyclable = "Recyclable"
    NonRecyclable = "NonRecyclable"

SERIAL_PORT = '/dev/ttyACM0' # Hardcoded 
servo_conn = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
async def trigger_servo(command: ServoCommand):
    try:
        response = str.encode(f'{command}\r\n')
        servo_conn.write(response)
        print(f"Response {response} successfully sent")
    except Exception as e:
        print(f"Error in trigger_servo: {e}")

router  = APIRouter(prefix="/servo")

@router.get("/")
async def test_servo(recyclable: bool):
    is_recyclable = ServoCommand.Recyclable if recyclable else ServoCommand.NonRecyclable
    trigger_servo(is_recyclable)
