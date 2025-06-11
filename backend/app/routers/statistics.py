"""
#HIỆN BIỂU ĐỒ
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.core.database import SessionLocal
from app.models.organization import Organization
from app.models.period import Period
from app.models.data_entry import DataEntry
import pandas as pd
from fastapi.responses import FileResponse
from io import BytesIO


router = APIRouter(prefix="/stats", tags=["Thống kê"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ranking/")
def get_ranking(period_id: int, db: Session = Depends(get_db)):
    
    #Trả về danh sách xếp hạng đơn vị theo tổng điểm của kỳ được chọn.
    
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        return {"error": f"Kỳ period_id={period_id} không tồn tại."}

    results = (
        db.query(
            Organization.name.label("organization"),
            func.sum(DataEntry.value).label("total_score")
        )
        .join(DataEntry, DataEntry.organization_id == Organization.id)
        .filter(DataEntry.period_id == period_id)
        .group_by(Organization.name)
        .order_by(desc("total_score"))
        .all()
    )

    # CHUYỂN về danh sách dict đúng chuẩn JSON
    return [
        {"organization": r.organization, "total_score": float(r.total_score or 0)}
        for r in results
    ]

    
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.data_entry import DataEntry
from app.core.database import SessionLocal
from sqlalchemy import func
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse

router = APIRouter(prefix="/stats", tags=["Thống kê"])

# Cấu hình logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ranking/")
def get_ranking(period_id: int, db: Session = Depends(get_db)):
    """
    Lấy bảng xếp hạng theo kỳ báo cáo
    """
    try:
        results = (
            db.query(
                Organization.name.label("organization"),
                func.sum(DataEntry.value).label("total_score")
            )
            .join(DataEntry, DataEntry.organization_id == Organization.id)
            .filter(DataEntry.period_id == period_id)
            .group_by(Organization.name)
            .order_by(func.sum(DataEntry.value).desc())
            .all()
        )

        logger.debug(f"Results: {results}")  # Log kết quả truy vấn
        
        return {"data": results}
    except Exception as e:
        logger.error(f"Error in getting ranking: {e}")
        return {"error": "Có lỗi xảy ra khi lấy bảng xếp hạng."}

@router.get("/export_excel/")
def export_excel(period_id: int, db: Session = Depends(get_db)):
    """
    Xuất báo cáo Excel từ bảng xếp hạng của kỳ báo cáo
    """
    try:
        results = (
            db.query(
                Organization.name.label("organization"),
                func.sum(DataEntry.value).label("total_score")
            )
            .join(DataEntry, DataEntry.organization_id == Organization.id)
            .filter(DataEntry.period_id == period_id)
            .group_by(Organization.name)
            .order_by(func.sum(DataEntry.value).desc())
            .all()
        )

        logger.debug(f"Results: {results}")  # Log kết quả truy vấn
        
        # Tạo DataFrame
        df = pd.DataFrame(results, columns=["organization", "total_score"])

        # Xuất ra file Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Bảng xếp hạng")
        
        output.seek(0)
        return FileResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="bang_xep_hang.xlsx")
    
    except Exception as e:
        logger.error(f"Error in exporting excel: {e}")
        return {"error": "Có lỗi xảy ra khi xuất báo cáo Excel."}

@router.get("/export_pdf/")
def export_pdf(period_id: int, db: Session = Depends(get_db)):
    """
    Xuất báo cáo PDF từ bảng xếp hạng của kỳ báo cáo
    """
    try:
        results = (
            db.query(
                Organization.name.label("organization"),
                func.sum(DataEntry.value).label("total_score")
            )
            .join(DataEntry, DataEntry.organization_id == Organization.id)
            .filter(DataEntry.period_id == period_id)
            .group_by(Organization.name)
            .order_by(func.sum(DataEntry.value).desc())
            .all()
        )

        logger.debug(f"Results: {results}")  # Log kết quả truy vấn

        # Tạo PDF
        file_path = "bang_xep_hang.pdf"
        c = canvas.Canvas(file_path, pagesize=(595, 842))  # Kích thước trang A4
        c.setFont("Helvetica", 12)

        c.drawString(100, 750, "Bảng xếp hạng theo kỳ Quý 1/2025")
        c.drawString(100, 730, "------------------------------------")
        
        y_position = 710
        for index, row in enumerate(results, 1):
            c.drawString(100, y_position, f"{index}. {row.organization} - {row.total_score} điểm")
            y_position -= 20

        c.save()

        return FileResponse(file_path, media_type="application/pdf", filename="bang_xep_hang.pdf")
    
    except Exception as e:
        logger.error(f"Error in exporting PDF: {e}")
        return {"error": "Có lỗi xảy ra khi xuất báo cáo PDF."}
