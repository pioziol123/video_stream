import asyncio
import websockets

receivers = set()


async def sendPicture(picture):
    try:
        for receiver in receivers:
            await receiver.send(picture)
    except Exception:
        receivers.remove(receiver)


async def handleMessage(websocket, path):
    async for message in websocket:
        if message == "receiver":
            receivers.add(websocket)
        elif websocket not in receivers:
            await sendPicture(message)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(handleMessage, "localhost", 8765)
)
asyncio.get_event_loop().run_forever()
