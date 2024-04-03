import asyncio
import base64

from collections import deque

import cv2
import websockets


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


async def start_client():
    async for websocket in websockets.connect('ws://localhost:8001'):
        try:
            for j in range(32*100):
                _, img = cap.read()
                resize = cv2.resize(img, (224, 224))
                retval, buffer = cv2.imencode('.jpg', resize)
                jpg_as_text = base64.b64encode(buffer)
                await websocket.send(jpg_as_text)
        except websockets.ConnectionClosed:
            continue


gestures_deque = deque(maxlen=5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for i in range(1):
        loop.create_task(start_client())

    loop.run_forever()

