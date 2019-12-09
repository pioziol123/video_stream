import cv2
import asyncio
import websockets
from io import BytesIO
import numpy as np
from base64 import b64encode
import time
import zmq
from zmq.asyncio import Context, ZMQEventLoop

ctx =Context()
vc = cv2.VideoCapture(0)
if not vc.isOpened():
    exit()


async def stream():
    socket = ctx.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")
    rval = True
    result = True
    while rval and result:
        rval, frame = vc.read()
        result, image = cv2.imencode(".jpg", frame)
        await socket.send_multipart([b"1", b64encode(image.tobytes())])
        await asyncio.sleep(1000/15000)

asyncio.set_event_loop(ZMQEventLoop())
asyncio.get_event_loop().run_until_complete(stream())
