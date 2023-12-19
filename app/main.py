import asyncio
import typing
from starlette.endpoints import WebSocketEndpoint
from fastapi import Depends, FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import models
from routes import project_routes, task_routes, user_routes
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import crud
from utils import get_db
import users_view, project_view, task_view

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(project_routes.router, prefix="/projects", tags=["projects"])
app.include_router(task_routes.router, prefix="/tasks", tags=["tasks"])
app.include_router(users_view.router, tags=["user_view"])
app.include_router(project_view.router, tags=["project_view"])
app.include_router(task_view.router, tags=["task_view"])


@app.on_event("startup")
async def startup_event():
    app.user_queue = asyncio.Queue()
    app.project_queue = asyncio.Queue()
    app.task_queue = asyncio.Queue()


async def send_user_event(websocket: WebSocket):
    queue = websocket.app.user_queue
    while True:
        print("Called background")
        data = await queue.get()
        await ws_app.broadcast(data)


async def send_project_event(websocket: WebSocket) -> None:
    queue = websocket.app.project_queue
    while True:
        print("Called background")
        data = await queue.get()
        await ws_app1.broadcast(data)


async def send_task_event(websocket: WebSocket) -> None:
    queue = websocket.app.task_queue
    while True:
        print("Called background")
        data = await queue.get()
        await ws_app2.broadcast(data)


class WsApp(WebSocketEndpoint):
    encoding = "json"

    def __init__(self, type: str):
        self.type = type
        self.ws_client = []

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.ws_client.append(websocket)
        print(len(self.ws_client))
        data = []
        if self.type == "users":
            data = crud.get_users(next(get_db()))
            asyncio.create_task(send_user_event(websocket))
        elif self.type == "projects":
            data = crud.get_projects(next(get_db()))
            asyncio.create_task(send_project_event(websocket))
        elif self.type == "tasks":
            data = crud.get_tasks(next(get_db()))
            asyncio.create_task(send_task_event(websocket))
        await self.broadcast(data)

    async def broadcast(self, data):
        for client in self.ws_client:
            await client.send_json(jsonable_encoder(data))

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        data = crud.get_users(next(get_db()))
        await self.broadcast(data)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        if websocket in self.ws_client:
            self.ws_client.remove(websocket)


class WsAppFastAPI(WsApp):

    def __init__(self, type: str):
        super().__init__(type)

    def __call__(self, websocket: WebSocket):
        self.scope = websocket.scope
        self.receive = websocket.receive
        self.send = websocket.send
        return self


ws_app = WsAppFastAPI("users")
app.add_api_websocket_route("/ws/users", ws_app, dependencies=[Depends(get_db)])

ws_app1 = WsAppFastAPI("projects")
app.add_api_websocket_route("/ws/projects", ws_app1, dependencies=[Depends(get_db)])

ws_app2 = WsAppFastAPI("tasks")
app.add_api_websocket_route("/ws/tasks", ws_app2, dependencies=[Depends(get_db)])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
