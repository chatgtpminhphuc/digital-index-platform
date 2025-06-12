from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db, DataStore

router = APIRouter(prefix="/periods", tags=["Periods"])

@router.get("/")
def list_periods(index_id: str = None, db: DataStore = Depends(get_db)):
    """Lấy danh sách các kỳ báo cáo. Có thể lọc theo mã bộ chỉ số (index_id)."""
    # Nếu truyền tham số index_id, trả về các kỳ của bộ chỉ số đó
    if index_id:
        periods = db.get_periods_by_index(index_id)
        if periods is None or len(periods) == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy kỳ báo cáo cho bộ chỉ số yêu cầu.")
        return periods
    # Nếu không truyền index_id, trả về tất cả các kỳ (kèm thông tin loại chỉ số)
    return db.get_all_periods()

@router.get("/indexes")
def list_indexes(db: DataStore = Depends(get_db)):
    """Lấy danh sách các bộ chỉ số (ví dụ: DTI, PAR Hành chính, PAR Sở GDĐT)."""
    result = []
    for idx_key, info in db.index_info.items():
        result.append({
            "id": idx_key,
            "name": info["name"]
        })
    return result
