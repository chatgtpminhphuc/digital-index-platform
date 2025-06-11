"""
# HIỆN BIỂU ĐỒ
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import indicators, data, statistics
from app.core.database import Base, engine
from app.routers import data

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hệ thống quản lý chỉ số",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(indicators.router)
app.include_router(data.router)
app.include_router(statistics.router)

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import statistics

app = FastAPI()

# Cấu hình CORS cho phép frontend truy cập backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cổng của frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(statistics.router)  # Router thống kê

# Cấu hình khi ứng dụng khởi động
@app.get("/")
def read_root():
    return {"message": "Hệ thống quản lý chỉ số hoạt động!"}
