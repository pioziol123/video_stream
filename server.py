import asyncio
import websockets
import zmq
from zmq.asyncio import Context, Poller, ZMQEventLoop

Url = 'tcp://127.0.0.1:5555'
Ctx = Context()
receivers = set()


async def sendPicture(picture):
    try:
        for receiver in receivers:
            await receiver.send(picture)
    except Exception as e:
        print(str(e))
        receivers.remove(receiver)


async def handleMessage(websocket, path):
    async for message in websocket:
        if websocket not in receivers:
            receivers.add(websocket)

async def handleZMQMessage():
    subscriber = Ctx.socket(zmq.SUB)
    subscriber.connect(Url)
    subscriber.setsockopt(zmq.SUBSCRIBE, b"1")
    poller = Poller()
    poller.register(subscriber, zmq.POLLOUT)
    while True:
        topic, data = await subscriber.recv_multipart()
        await sendPicture(data)

asyncio.set_event_loop(ZMQEventLoop())
asyncio.get_event_loop().run_until_complete(
    asyncio.gather(
        websockets.serve(handleMessage, "localhost", 8765),
        handleZMQMessage()
    )
)
# asyncio.get_event_loop().run_forever()
