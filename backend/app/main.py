from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, projects, tasks, comments

app = FastAPI()


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router)

