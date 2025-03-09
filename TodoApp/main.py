
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

#1. Khởi tạo ứng dụng FastAPI:
app = FastAPI()
# 2. Tạo bảng trong cơ sở dữ liệu:
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
