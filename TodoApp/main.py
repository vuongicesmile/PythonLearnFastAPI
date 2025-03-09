from typing import Annotated

from fastapi.params import Depends
# SQLAlchemy để tương tác với cơ sở dữ liệu
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Todos
from database import engine, SessionLocal

#1. Khởi tạo ứng dụng FastAPI:
app = FastAPI()
# 2. Tạo bảng trong cơ sở dữ liệu:
models.Base.metadata.create_all(bind=engine)

def get_db():
    #Đây là một đối tượng session được tạo ra từ SQLAlchemy để kết nối với cơ sở dữ liệu.
    db = SessionLocal()
    try:
        #Câu lệnh này trả về session cho một lần sử dụng trong các endpoint API
        yield db
    finally:
        # Đảm bảo rằng kết nối cơ sở dữ liệu sẽ được đóng sau khi hoàn thành việc sử dụng
        db.close()

@app.get("/")
#Đây là một hàm bất đồng bộ (asynchronous function). db là đối tượng Session (phiên làm việc) được lấy từ hàm get_db(). Depends(get_db) là cách FastAPI sử dụng để tự động tiêm đối tượng db vào hàm khi cần thiết.
async def read_all(db:Annotated[Session, Depends(get_db)]):
    # Dòng này thực hiện một truy vấn cơ sở dữ liệu để lấy tất cả các bản ghi từ bảng Todos. Kết quả trả về là một danh sách tất cả các công việc trong bảng Todos.
    return db.query(Todos).all()