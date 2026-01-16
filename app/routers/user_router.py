from fastapi import APIRouter, HTTPException,UploadFile, File, status
from typing import List, Dict
from app.models.user_model import UserCreate, UserResponse
from app.services.user_service import user_service

"""
實現模組化，這裡建立 API 的路徑，並呼叫 services 內定義過的行為
"""

# 建立路由器，並加入網址的前綴，後續 API 都會由此前綴開始
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- 以下開始路由每個 API ---

# /users
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,  # 回傳 201，代表成功且有新資料建立
    summary="Create a new user",
    description="""
    Create a new user with name and age. Requires validation.
    1. name: not empty.
    2. age: between 0 and 120.
    """,
    response_description="User created successfully"
)
async def create_user(user: UserCreate):
    """
    新增使用者
    """
    return user_service.create_user(user)

# users/{name}
@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user by name",
    response_description="User deleted successfully"
)
async def delete_user(name: str):
    success = user_service.delete_user_by_name(name)
    # 代表 service 端函式回傳的是 false，刪除失敗
    if not success:
        raise HTTPException(status_code=404, detail=f"User {name} not found")
    return   # 204 不回傳 content

# users/all
@router.get(
    "/all",
    response_model=List[UserResponse],  # service 裡該函式返回的是 List
    summary="Get all users",
    description="Retrieve a list of users who have been added before"
)
async def get_users() -> List[UserResponse]:
    return user_service.get_all_users()

# users/upload
@router.post(
    "/upload",
    response_model=List[UserCreate],
    summary="Upload users CSV file",
    description="Upload a CSV file to add multiple users at once",
    response_description="Multiple users added successfully"
)
# 用 UploadFile 包裝上傳的檔案，避免檔案過大佔據記憶體
async def upload_users(file: UploadFile = File(...)):
    content = await file.read()  # 讀取檔案，型別變成 bytes
    try: 
        return user_service.process_csv_upload(content) # 呼叫 process_csv_upload 方法以處理多位 users 的加入
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV file: {str(e)}")

# users/average-age
@router.get(
    "/average-age",
    summary="Get average age by group",
    description="""
    1. Group users by the first character of their name.
    2. Calculate the average age of each group.
    """
)
async def get_average_age() -> Dict[str, float]:
    return user_service.get_average_age_by_group()

