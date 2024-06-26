import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from api.controllers.combos import ComboController
from api.controllers.socket.ConnectionManager import ConnectionManager
from api.controllers.star import StarController
from api.controllers.video import VideoController
from api.core import PornHub
from api.middleware.cacheInterceptor import intercept_all_requests
from api.middleware.cors import setup_cors
from api.middleware.timeCount import add_process_time_header

logging.config.fileConfig('api/logConfig.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI(title='Potential Octo Fiesta', version='1.0.0')
client = PornHub([])

# Middleware
app.middleware("http")(intercept_all_requests)
app.middleware("http")(add_process_time_header)


@app.get("/health")
async def read_health():
    return {"status": "OK"}


# CORS
setup_cors(app)

app.include_router(StarController.router)
app.include_router(VideoController.router)
app.include_router(ComboController.router)

manager = ConnectionManager()

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=int(8080), debug=True)
