from fastapi import FastAPI
from app.routers import user_router

"""
程式進入點，將 Router 掛載進來
"""

app = FastAPI(
    title="Backend Handsome Practice",
    description=""
)

# 將 Router 掛載進來
app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn
    # 啟動伺服器
    uvicorn.run(app, host="0.0.0.0", port=8000)