# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, projects, tasks, comments


app = FastAPI()

# ----------------------
# CORS 設定
# ----------------------
FRONTEND_URL = os.getenv("FRONTEND_URL")  # デフォルトは Vite のローカル

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # 許可するオリジン
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE などすべて
    allow_headers=["*"],  # 全ヘッダーを許可
)

# ----------------------
# ルーター登録
# ----------------------
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router)