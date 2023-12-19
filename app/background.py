# import asyncio
# import typing
# from starlette.endpoints import WebSocketEndpoint
# from fastapi import Depends, FastAPI, Request, Form, WebSocket
# from fastapi.encoders import jsonable_encoder
# import crud
# from utils import get_db
#
#
# async def send_event(websocket: WebSocket) -> None:
#     user_queue = websocket.app.user_queue
#     while True:
#         print("Called background")
#         data = await user_queue.get()
#         await ws_app.broadcast(data)
#
#
# class WsApp(WebSocketEndpoint):
#     encoding = "json"
#     ws_client = []
#
#     def __init__(self):
#         pass
#
#     async def on_connect(self, websocket: WebSocket) -> None:
#         await websocket.accept()
#         self.ws_client.append(websocket)
#         data = crud.get_users(next(get_db()))
#         await asyncio.create_task(send_event(websocket))
#         await self.broadcast(data)
#
#     async def broadcast(self, data):
#         for client in self.ws_client:
#             await client.send_json(jsonable_encoder(data))
#
#     async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
#         data = crud.get_users(next(get_db()))
#         await self.broadcast(data)
#
#     async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
#         if websocket in self.ws_client:
#             self.ws_client.remove(websocket)