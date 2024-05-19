import asyncio
import base64
import time

from collections import deque

import cv2
import websockets


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
counter = 1


async def wait_for_message(websocket):
    print(await websocket.recv())


async def start_client():
    start_time = time.time()
    async with websockets.connect('ws://localhost:8001') as websocket:
        for j in range(32*100):
            _, img = cap.read()
            resize = cv2.resize(img, (224, 224))
            retval, buffer = cv2.imencode('.jpg', resize)
            jpg_as_text = base64.b64encode(buffer)
            await websocket.send(jpg_as_text)
            # if j > 32:
            #     try:
            #         await asyncio.wait_for(wait_for_message(websocket), timeout=0.01)
            #         print(time.time() - start_time)
            #     except asyncio.TimeoutError:
            #         pass
        print(time.time() - start_time)
        print("closed")


gestures_deque = deque(maxlen=5)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    for i in range(5):
        loop.create_task(start_client())

    loop.run_forever()
