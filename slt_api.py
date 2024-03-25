import asyncio
import base64
import json
import uuid
import cProfile
import numpy as np
import websockets
import threading
import time
from collections import deque
from multiprocessing import Pool, Process
import cv2
from model import Predictor
from utils import SLInference
import logging

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

MAX_THREADS = 1
model: Predictor | None = None
user_count = 0
prof = cProfile.Profile()


def init_model(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    global model
    model = Predictor(config)


def process_images():
    pass


async def handler(websocket: websockets.WebSocketCommonProtocol):
    user_id = uuid.uuid4()
    global user_count
    user_count += 1
    image_queue = deque(maxlen=32)
    async for message in websocket:
        image_bytes = base64.b64decode(message)
        frame = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(frame, 1)

        image_queue.append(image)
        print(threading.active_count())
        if len(image_queue) == 32:
            results = model.predict(image_queue)
            if results:
                await websocket.send(str(results))
                print(user_id, results)
    #event = json.loads(message)


async def main():
    async with websockets.serve(handler, "localhost", 8001, ping_interval=None):
        await asyncio.Future()

if __name__ == "__main__":
    init_model("configs/config.json")
    asyncio.run(main())


