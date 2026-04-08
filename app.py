from fastapi import FastAPI
from contextlib import asynccontextmanager
from env import ScamDefenseEnv
from models import Action

env = ScamDefenseEnv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await env.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "AegisAI OpenEnv Server is running!"}

@app.get("/reset")
@app.post("/reset")
async def reset():
    return await env.reset()

@app.post("/step")
async def step(action: Action):
    return await env.step(action)

@app.get("/state")
async def state():
    return await env.state()
