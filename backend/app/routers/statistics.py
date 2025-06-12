from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.database import get_db, DataStore

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/ranking/")
def get_ranking(period_id: int, db: DataStore = Depends(get_db)):
    """Lấy bảng xếp hạng đơn vị theo kỳ báo cáo (period_id)."""
    data = db.get_ranking(period_id)
    if data is None:
        # 404 Not Found nếu period_id không tồn tại hoặc không có dữ liệu
        raise HTTPException(status_code=404, detail="Kỳ báo cáo không tồn tại hoặc chưa có dữ liệu.")
    return data  # trả về list các đơn vị với điểm và rank

@router.get("/export_excel/")
def export_excel(period_id: int, db: DataStore = Depends(get_db)):
    """Xuất báo cáo Excel cho kỳ báo cáo (period_id)."""
    data = db.get_ranking(period_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Kỳ báo cáo không tồn tại hoặc dữ liệu rỗng.")
    try:
        # Tạo DataFrame từ data và ghi vào file Excel (trả về qua StreamingResponse)
        import pandas as pd
        df = pd.DataFrame(data)
        # Đặt tên các cột tiếng Việt cho đẹp (tùy chọn)
        df = df.rename(columns={"unit": "Đơn vị", "score": "Tổng điểm", "rank": "Thứ hạng"})
        output = pd.ExcelWriter("report.xlsx", engine="openpyxl")
        df.to_excel(output, index=False, sheet_name="Report")
        output.close()
        excel_file = open("report.xlsx", "rb")
        # Thiết lập header để tải về file
        headers = {"Content-Disposition": "attachment; filename=report.xlsx"}
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    except Exception as e:
        print(f"Lỗi export_excel: {e}")
        raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xuất báo cáo Excel.")

@router.get("/export_pdf/")
def export_pdf(period_id: int, db: DataStore = Depends(get_db)):
    """Xuất báo cáo PDF cho kỳ báo cáo (period_id). (Chưa hỗ trợ)"""
    # Hiện tại chưa triển khai xuất PDF, trả về mã 501 Not Implemented
    raise HTTPException(status_code=501, detail="Chức năng xuất PDF chưa được hỗ trợ.")
