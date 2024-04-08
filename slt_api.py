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


def init_model(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    global model
    model = Predictor(config)


def process_image(image: bytes):
    image_bytes = base64.b64decode(image)
    frame = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(frame, -1)
    return image


async def handler(websocket: websockets.WebSocketCommonProtocol):
    image_queue = deque(maxlen=32)
    try:
        async for message in websocket:
            await websocket.ensure_open()
            image_queue.append(await asyncio.to_thread(process_image, message))
            if len(image_queue) == 32:
                res = await asyncio.to_thread(model.predict, image_queue)
                if res is not None and res['labels'][0] != 'no':
                    print(str(res))
                    await websocket.send(str(res))
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    async with websockets.serve(handler, "localhost", 8001, ping_interval=None):
        await asyncio.Future()

if __name__ == "__main__":
    init_model("configs/config.json")
    asyncio.run(main())


