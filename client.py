import cv2
import asyncio
import websockets
from io import BytesIO
import numpy as np
from base64 import b64encode

vc = cv2.VideoCapture(0)
if not vc.isOpened():
    exit()


async def stream():
    async with websockets.connect("ws://localhost:8765") as websocket:
        rval = True
        result = True
        while rval and result:
            rval, frame = vc.read()
            result, image = cv2.imencode(".png", frame)
            await websocket.send(b64encode(image.tobytes()))


asyncio.get_event_loop().run_until_complete(stream())
