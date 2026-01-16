import pandas as pd
from typing import List, Dict, Optional
from app.models.user_model import UserCreate, UserResponse
import io

class UserService:
    """
    實作 API 邏輯、運算、取值等等操作
    """
    def __init__(self):
        # 用 List 模擬資料庫，裡面 user 資料包裝成 dict，並讓他存在 In-memory
        self._users: List[dict] = []

    def create_user(self, user: UserCreate) -> UserResponse:
        """
        新增 user (POST API)，
        在 user 傳入前就會先做 UserCreate 物件的驗證
        """
        new_user = user.model_dump()   # 將 UserCreate 轉換為 dict 格式
        self._users.append(new_user)
        return UserResponse(**new_user) # 將 dict 轉換為 UserResponse 格式傳入
    
    def delete_user_by_name(self, name: str) -> bool:
        """
        根據特定 name 刪除 user (DELETE API)
        """

        initial_count = len(self._users)

        # 只保留名字不是傳入 name 的使用者 (等同於刪除)
        self._users = [user for user in self._users if user["name"] != name]
        # 如果 user 數量變少，代表刪除成功，返回 True
        return len(self._users) < initial_count

    def process_csv_upload(self, file: bytes) -> List[UserCreate]:  # 接收的是 bytes 格式
        """
        透過 API 上傳 CSV 檔，以新增多位 user (POST API)
        """
        # 讀取 Byte 串流
        df = pd.read_csv(io.BytesIO(file))

        # 檢查上傳檔案的欄位是否符合格式
        if 'Name' not in df.columns or 'Age' not in df.columns:
            raise ValueError("CSV format error: header is not correct")

        new_users_list = []
        for idx, row in df.iterrows():
            user_data = {"name": row["Name"], "age": row["Age"]}
            self._users.append(user_data)
            new_users_list.append(UserCreate(**user_data))  # 用 ** 解包 dict

        return new_users_list

    def get_all_users(self) -> List[UserResponse]:
        """
        取得所有 user (GET API)
        """

        return [UserResponse(**user) for user in self._users]
    
    def get_average_age_by_group(self) -> Dict[str, float]:
        """
        將 user 分組並計算每一組中的平均年齡 (GET API)
        """

        if not self._users:
            return {}
        df = pd.DataFrame(self._users)
        # 新增欄位用於分組，取 name 的第一個字元作為標準
        df['group_key'] = df['name'].str[0]
        df_grouped = df.groupby('group_key')

        result = df_grouped['age'].mean()   # 計算每組的年齡平均
        return result.to_dict()
    
# 建立全域物件供 Router 使用
user_service = UserService()

