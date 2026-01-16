from pydantic import BaseModel, Field

"""
用 pydantic 建立 data model，方便做資料驗證與資料解析
"""
class UserCreate(BaseModel):
    """
    接收"建立使用者"請求的模型 (Request Body)
    """
    # 用 Field 建立 Swagger 上的 API 文件描述，並設定兩個變數的驗證歸則
    name: str = Field(..., description="User name", min_length=1) # not empty
    age: int = Field(..., description="User age", ge=1, le=120)   # between 1 and 120

    # 建立範例，讓 Swagger UI 上有範例
    model_config = {
        'json_schema_extra': {
            "examples": [
                {
                    "name": "Jason",
                    "age": 23
                }
            ]
        }
    }

class UserResponse(BaseModel):
    """
    回應使用者資料的模型 (Response Body)
    """
    name: str
    age: int