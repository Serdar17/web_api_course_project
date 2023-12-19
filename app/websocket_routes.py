# from starlette.websockets import WebSocket
# import crud
# import json
# from database import SessionLocal, engine
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Form, WebSocket, WebSocketDisconnect
# from fastapi.encoders import jsonable_encoder
# import schemas
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# router = APIRouter()
#
#
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
#
#     async def broadcast(self, message):
#         for connection in self.active_connections:
#             await connection.send_json(message)
#
#
# manager = ConnectionManager()
#
#
# async def notify_clients(message: str):
#     for connection in manager.active_connections:
#         await connection.send_text(message)
#
#
# @router.websocket_route("/ws")
# async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
#     await manager.connect(websocket)
#     # await manager
#     try:
#         while True:
#             # data = await websocket.receive_text()
#             # db = get_db()
#             data = crud.get_users(next(get_db()))
#             users = data[0]
#             # users = schemas.User(name="srtr", email="asdasda")
#             users = jsonable_encoder(users)
#
#             await websocket.send_json(users)
#             # await manager.send_personal_message(f"You wrote: {data}", websocket)
#             # await manager.broadcast(data)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)