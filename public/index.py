from fastapi import FastAPI

from src.routes import register_routes

app = FastAPI()



register_routes(app)



