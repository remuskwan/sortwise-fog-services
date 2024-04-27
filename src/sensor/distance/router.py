from fastapi import APIRouter
import os
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

router = APIRouter(
    prefix="/distance",
    tags=["distance", "ultrasonic"],
    responses={404: {"description": "Not found"}},
)
# Load environment variables
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_DISTANCE_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


@router.on_event("startup")
async def startup_event():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)


@router.post("/publish/")
async def publish_message(payload: dict):
    client.publish(MQTT_TOPIC, payload=json.dumps(payload))
    return {"message": "Message published", "data": payload}
