from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import os
from dotenv import load_dotenv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
load_dotenv()


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
    myMQTTClient = AWSIoTMQTTClient(
        os.getenv("IOT_CORE_THING_NAME"))  # Use your Thing Name here
    # Use your AWS IoT Core endpoint here
    myMQTTClient.configureEndpoint(
        os.getenv("IOT_CORE_ENDPOINT"), 8883)
    # Update paths to your downloaded files
    myMQTTClient.configureCredentials(
        os.getenv("IOT_CORE_ROOT_CA_PATH"), os.getenv("IOT_CORE_PRIVATE_KEY_PATH"), os.getenv("IOT_CORE_CERTIFICATE_PATH"))

    # Connect and subscribe to AWS IoT
    myMQTTClient.connect()
    myMQTTClient.subscribe(os.getenv("IOT_CORE_TOPIC"), 1, handle_iot_message)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    loop.create_task(start_iot_client())
