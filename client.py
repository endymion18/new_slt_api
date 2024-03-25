import asyncio
import base64
import json
from collections import deque

import cv2
import websockets


async def start_client():
    async for websocket in websockets.connect('ws://localhost:8001'):
        try:
            cap = cv2.VideoCapture(1)

            for j in range(32*100):
                _, img = cap.read()
                resize = cv2.resize(img, (224, 224))
                retval, buffer = cv2.imencode('.jpg', resize)
                jpg_as_text = base64.b64encode(buffer)
                await websocket.send(jpg_as_text)
                if j % 32 == 0 and j != 0:
                    print(await websocket.recv())
        except websockets.ConnectionClosed:
            continue


gestures_deque = deque(maxlen=5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for i in range(100):
        loop.create_task(start_client())

    loop.run_forever()

