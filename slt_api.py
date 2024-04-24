import asyncio
import base64
import json

import numpy as np
import websockets
from collections import deque
import cv2
from model import Predictor

import logging

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

users = {}
model: Predictor | None = None
loop = asyncio.new_event_loop()


def init_model(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    global model
    model = Predictor(config)


def process_image(image: bytes):
    image_bytes = base64.b64decode(image)
    frame = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(frame, 1)
    return image


def prediction(websocket: websockets.WebSocketServerProtocol):
    while True:
        if websocket.closed:
            break
        if len(users[websocket.id]) == 32:
            images = [process_image(image) for image in users[websocket.id].copy()]
            res = model.predict(images)
            if res is not None and res['labels'][0] != 'no':
                asyncio.run(websocket.send(json.dumps(res['labels'])))
                users[websocket.id].clear()


async def handler(websocket: websockets.WebSocketServerProtocol):
    users[websocket.id] = deque(maxlen=32)
    loop.run_in_executor(None, prediction, websocket)
    try:
        async for message in websocket:
            await websocket.ensure_open()
            users[websocket.id].append(message)
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    async with websockets.serve(handler, "localhost", 8001, ping_interval=None, max_queue=2**8):
        await asyncio.Future()

if __name__ == "__main__":
    init_model("configs/config.json")
    asyncio.run(main())


