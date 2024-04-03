from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Allows React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


def handle_iot_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        logger.info(f"Received message from IoT Core: {msg}")
        asyncio.run(manager.broadcast(msg))
    except Exception as e:
        logger.error(f"Error handling message: {e}")


async def start_iot_client():
    # Initialize the MQTT client
    myMQTTClient = AWSIoTMQTTClient("remus_rpi4")  # Use your Thing Name here
    # Use your AWS IoT Core endpoint here
    myMQTTClient.configureEndpoint(
        "a1zij3hvzjwttw-ats.iot.ap-southeast-1.amazonaws.com", 8883)
    # Update paths to your downloaded files
    myMQTTClient.configureCredentials(
        "/home/pi/Documents/aws-iot-core-credentials/root-CA.crt", "/home/pi/Documents/aws-iot-core-credentials/remus_rpi4.private.key", "/home/pi/Documents/aws-iot-core-credentials/remus_rpi4.cert.pem")

    # Connect and subscribe to AWS IoT
    myMQTTClient.connect()
    myMQTTClient.subscribe("inference/results", 1, handle_iot_message)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    loop.create_task(start_iot_client())
