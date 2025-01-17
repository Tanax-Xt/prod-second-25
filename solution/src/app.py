import os

import uvicorn
from fastapi import FastAPI

from solution.src.api import api_router
from solution.src.db import ENGINE, Base


Base.metadata.create_all(ENGINE)

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
