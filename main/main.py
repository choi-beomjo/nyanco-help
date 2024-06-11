from fastapi import FastAPI
import uvicorn

from api.api import api

app = FastAPI()

app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app)