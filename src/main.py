import uvicorn
from fastapi import FastAPI
from src.api import main_router as router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)