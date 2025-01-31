from fastapi import FastAPI
from src.infra.api.routes import webhook_router


from fastapi.concurrency import asynccontextmanager


@asynccontextmanager
async def set_lifespan(app: FastAPI):
    try:
        from pyngrok import ngrok

        port = 8000
        tunnel = ngrok.connect(port)
        public_url = tunnel.public_url
        print(f"ngrok tunnel '{public_url}' -> 'http://127.0.0.1:{port}'")
        yield
    finally:
        ngrok.disconnect(public_url)


app = FastAPI(lifespan=set_lifespan)

# app = FastAPI()
app.include_router(webhook_router, tags=["webhook"])
