from typing import Annotated
from fastapi.params import  Path
from pydantic import BaseModel, Field
# SQLAlchemy để tương tác với cơ sở dữ liệu
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, APIRouter
from starlette import status # using status
from models import Todos
from database import SessionLocal
from .auth import  get_current_user

# use router
#1. Khởi tạo ứng dụng FastAPI:
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


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
user_dependency = Annotated[dict, Depends(get_current_user)]

# validate request
class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt = 6)
    complete: bool

@router.get("/", status_code=status.HTTP_200_OK)
#Đây là một hàm bất đồng bộ (asynchronous function). db là đối tượng Session (phiên làm việc) được lấy từ hàm get_db(). Depends(get_db) là cách FastAPI sử dụng để tự động tiêm đối tượng db vào hàm khi cần thiết.
async def read_all(user: user_dependency, db:db_dependency):
    # Dòng này thực hiện một truy vấn cơ sở dữ liệu để lấy tất cả các bản ghi từ bảng Todos. Kết quả trả về là một danh sách tất cả các công việc trong bảng Todos.
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path
    (gt=0)): # Path(gt=0) : sử dụng path parameter từ FASTAPI, yêu cầu gt chỉ chấp nhận todo_id lớn hơn 0 (không có giá trị âm hoặc bằng 0)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return  todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, # thêm user dependancy
                      db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # add dictionary
    # lấy thêm user_id
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))


    # the db need to know ahead of time what func is about to happen
    # mean chuẩn bị sẵn csdl trong khi commit coomit xcxoas tất cả
    # và thật sự transtition đến DB
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                    todo_request: TodoRequest,
                    todo_id: int = Path(gt=0)): # phai de cuoi cung de verify
    # add dictionary
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail= 'Todo not found')

# phải đúng thự tự của json để ko tạo obj mới
    todo_model.description = todo_request.description
    todo_model.complete = todo_request.complete
    todo_model.title = todo_request.title
    todo_model.priority = todo_request.priority


    db.add(todo_model)
    db.commit()
    # the db need to know ahead of time what func is about to happen
    # mean chuẩn bị sẵn csdl trong khi commit coomit xcxoas tất cả
    # và thật sự transtition đến DB

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)

async def update_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()