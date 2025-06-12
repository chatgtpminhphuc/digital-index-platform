from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import statistics, period, data_entry

app = FastAPI(
    title="Digital Index Platform API",
    description="API backend cho Digital Index Platform",
    version="1.0.0"
)

# Cấu hình CORS cho phép frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả domain (có thể chỉnh cụ thể như ["http://localhost:5173"] để bảo mật hơn)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(statistics.router)
app.include_router(period.router)
app.include_router(data_entry.router)
