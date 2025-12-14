import time
import json
from fastapi import FastAPI
import uvicorn
import auth


app = FastAPI()

app.include_router(auth.router)


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )