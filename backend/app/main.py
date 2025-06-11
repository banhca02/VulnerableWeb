from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import urlparse

from app.api import user

app = FastAPI(
    title="User Management API",
    description="A simple CRUD API for managing users",
    version="1.0.0"
)

# Đăng ký router
app.include_router(user.router, prefix="/api")


origins_list = [
    "http://localhost",
    "http://localhost:5173", # Nếu frontend của bạn chạy ở đây
    "http://127.0.0.1",
    "http://127.0.0.1:8000", # Nếu frontend của bạn chạy ở đây
    # Thêm bất kỳ origin nào khác mà frontend của bạn có thể từ đó truy cập API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Quan trọng: cho phép OPTIONS và các methods khác
    allow_headers=["*"],  # Quan trọng: cho phép các headers cần thiết cho preflight
    max_age=600,          # Khuyên dùng: cache preflight response trong 10 phút
)

