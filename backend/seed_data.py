
#########___1. Thêm dữ liệu vào bảng Organization cho "Tỉnh B" và "Tỉnh C"


from app.core.database import SessionLocal
from app.models.organization import Organization

db = SessionLocal()


# Tạo mới tổ chức "Tỉnh A"
org_a = Organization(name="Tỉnh A", code="TINH_A")
db.add(org_a)
# Tạo mới tổ chức "Tỉnh B"
org_b = Organization(name="Tỉnh B", code="TINH_B")
db.add(org_b)

# Tạo mới tổ chức "Tỉnh C"
org_c = Organization(name="Tỉnh C", code="TINH_C")
db.add(org_c)

db.commit()  # Lưu vào DB
db.close()

#########___2. Thêm dữ liệu vào bảng Period cho kỳ "Quý 1/2025".

from app.models.period import Period
db = SessionLocal()
# Kiểm tra nếu kỳ "Quý 1/2025" đã có
period = db.query(Period).filter_by(code="Q1-2025").first()
if not period:
    period = Period(name="Quý 1/2025", code="Q1-2025", start_date="2025-01-01", end_date="2025-03-31")
    db.add(period)
    db.commit()
    db.refresh(period)
db.close()



#########___3. Thêm dữ liệu vào bảng Indicator (Chỉ số)
from app.models.indicator import Indicator
db = SessionLocal()
# Kiểm tra nếu chỉ số "DTI" đã có
indicator = db.query(Indicator).filter_by(code="DTI").first()
if not indicator:
    indicator = Indicator(code="DTI", name="Chuyển đổi số", description="DTI 2025")
    db.add(indicator)
    db.commit()
    db.refresh(indicator)
db.close()


#########___4. Thêm dữ liệu vào bảng DataEntry cho "Tỉnh B" và "Tỉnh C" với giá trị tương ứng
###############Giả sử giá trị điểm cho các tổ chức "Tỉnh B" và "Tỉnh C" là 95.0 và 88.5:
from app.models.data_entry import DataEntry

db = SessionLocal()

# Giả sử các ID của tổ chức "Tỉnh B", "Tỉnh C", kỳ "Q1-2025" và chỉ số "DTI" đã có
indicator_id = 1  # ID của chỉ số "DTI"
period_id = 1  # ID của kỳ "Q1-2025"

# Thêm dữ liệu cho Tỉnh A
org_a_id = 1  # ID của tổ chức "Tỉnh A"
entry_a = DataEntry(indicator_id=indicator_id, organization_id=org_a_id, period_id=period_id, value=55.0)
db.add(entry_a)


# Thêm dữ liệu cho Tỉnh B
org_b_id = 2  # ID của tổ chức "Tỉnh B"
entry_b = DataEntry(indicator_id=indicator_id, organization_id=org_b_id, period_id=period_id, value=95.0)
db.add(entry_b)

# Thêm dữ liệu cho Tỉnh C
org_c_id = 3  # ID của tổ chức "Tỉnh C"
entry_c = DataEntry(indicator_id=indicator_id, organization_id=org_c_id, period_id=period_id, value=88.5)
db.add(entry_c)

db.commit()  # Lưu vào DB
db.close()


"""


################# 1. Xóa dữ liệu trong bảng Organization (Tổ chức)
#Để xóa dữ liệu của Tỉnh B và Tỉnh C, bạn thực hiện như sau:
from app.core.database import SessionLocal
from app.models.organization import Organization
db = SessionLocal()
# Xóa tổ chức "Tỉnh B"
org_b = db.query(Organization).filter_by(code="TINH_B").first()
if org_b:
    db.delete(org_b)
    db.commit()
# Xóa tổ chức "Tỉnh C"
org_c = db.query(Organization).filter_by(code="TINH_C").first()
if org_c:
    db.delete(org_c)
    db.commit()
db.close()

################# 2. Xóa dữ liệu trong bảng Period (Kỳ báo cáo)
#Để xóa dữ liệu của kỳ "Quý 1/2025", bạn làm như sau:
from app.core.database import SessionLocal
from app.models.period import Period
db = SessionLocal()
# Xóa kỳ "Quý 1/2025"
period = db.query(Period).filter_by(code="Q1-2025").first()
if period:
    db.delete(period)
    db.commit()
db.close()

################# 3. Xóa dữ liệu trong bảng Indicator (Chỉ số)
#Để xóa chỉ số "DTI":
from app.core.database import SessionLocal
from app.models.indicator import Indicator
db = SessionLocal()
# Xóa chỉ số "DTI"
indicator = db.query(Indicator).filter_by(code="DTI").first()
if indicator:
    db.delete(indicator)
    db.commit()
db.close()

################# 4. Xóa dữ liệu trong bảng DataEntry (Dữ liệu nhập)
#Để xóa dữ liệu của "Tỉnh B" và "Tỉnh C" cho kỳ "Quý 1/2025" và chỉ số "DTI":
from app.core.database import SessionLocal
from app.models.data_entry import DataEntry
db = SessionLocal()
# Xóa dữ liệu của Tỉnh B trong kỳ "Q1-2025"
entry_b = db.query(DataEntry).filter_by(organization_id=2, period_id=1, indicator_id=1).first()  # Giả sử ID tổ chức Tỉnh B là 2
if entry_b:
    db.delete(entry_b)
    db.commit()
# Xóa dữ liệu của Tỉnh C trong kỳ "Q1-2025"
entry_c = db.query(DataEntry).filter_by(organization_id=3, period_id=1, indicator_id=1).first()  # Giả sử ID tổ chức Tỉnh C là 3
if entry_c:
    db.delete(entry_c)
    db.commit()
db.close()

################# 5. Xóa tất cả dữ liệu trong bảng
#Nếu bạn muốn xóa toàn bộ dữ liệu trong một bảng, bạn có thể làm như sau:
from app.core.database import SessionLocal
from app.models.organization import Organization
db = SessionLocal()
# Xóa tất cả dữ liệu trong bảng Organization
db.query(Organization).delete()
db.commit()
db.close()

"""
