from typing import Annotated

from fastapi.params import Depends, Path
# SQLAlchemy để tương tác với cơ sở dữ liệu
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from starlette import status # using status

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
       # trả về ngay lập tức thay về lặp qua tất cả rồi mới trả về
        yield db
    finally:
        # Đảm bảo rằng kết nối cơ sở dữ liệu sẽ được đóng sau khi hoàn thành việc sử dụng
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
#Đây là một hàm bất đồng bộ (asynchronous function). db là đối tượng Session (phiên làm việc) được lấy từ hàm get_db(). Depends(get_db) là cách FastAPI sử dụng để tự động tiêm đối tượng db vào hàm khi cần thiết.
async def read_all(db:db_dependency):
    # Dòng này thực hiện một truy vấn cơ sở dữ liệu để lấy tất cả các bản ghi từ bảng Todos. Kết quả trả về là một danh sách tất cả các công việc trong bảng Todos.
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path
    (gt=0)): # Path(gt=0) : sử dụng path parameter từ FASTAPI, yêu cầu gt chỉ chấp nhận todo_id lớn hơn 0 (không có giá trị âm hoặc bằng 0)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return  todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')
