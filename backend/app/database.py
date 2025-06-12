from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Cấu hình kết nối PostgreSQL
DATABASE_URL = "postgresql://postgres:Thangpassword@localhost:5432/digital_index_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Hàm get_db để dùng trong dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Class mô phỏng một kho dữ liệu (DataStore), tùy bạn có thể dùng hay bỏ
class DataStore:
    def __init__(self, db: Session):
        self.db = db
import pandas as pd

# Thông tin các bộ chỉ số và file dữ liệu tương ứng
index_info = {
    "dti": {
        "name": "Chỉ số Chuyển đổi số",
        "file": "DTI.xlsx"
    },
    "par_hsh": {
        "name": "PAR Index khối Hành chính",
        "file": "ParIndex_hsh.xls"
    },
    "par_sgddt": {
        "name": "PAR Index khối Sở GDĐT",
        "file": "ParIndex_sgddt.xls"
    }
}

class DataStore:
    def __init__(self):
        self.index_info = index_info
        # self.data sẽ lưu dữ liệu các bảng xếp hạng theo từng bộ chỉ số và kỳ
        self.data = {}  # cấu trúc: data[index_key]["periods"][year] = list of {unit, score, rank}
        self.period_map = {}    # ánh xạ period_id (toàn cục) -> (index_key, year)
        self.periods_list = []  # danh sách tất cả các kỳ (bao gồm index) với id
        self._load_data()

    def _load_data(self):
        """Đọc dữ liệu từ các file Excel và lưu vào self.data, self.period_map, self.periods_list."""
        period_id = 1
        for idx_key, info in self.index_info.items():
            file_path = info["file"]
            try:
                # Đọc tất cả sheet trong file Excel
                xls = pd.ExcelFile(file_path)
            except Exception as e:
                print(f"Lỗi khi đọc file {file_path}: {e}")
                continue
            for sheet_name in xls.sheet_names:
                try:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                except Exception as e:
                    print(f"Lỗi khi đọc sheet '{sheet_name}' từ {file_path}: {e}")
                    continue
                if df is None or df.empty:
                    continue
                # Xác định tên cột chứa đơn vị và cột chứa điểm
                unit_col = None
                score_col = None
                for col in df.columns:
                    col_name = str(col).lower()
                    if "đơn vị" in col_name or "don vi" in col_name or "đơnvị" in col_name or "tỉnh" in col_name or "địa phương" in col_name or "unit" in col_name or "name" in col_name:
                        unit_col = col
                    if "tổng" in col_name or "tong" in col_name:
                        score_col = col
                # Nếu không tìm thấy "Tổng điểm", tìm cột chứa "điểm"
                if score_col is None:
                    for col in df.columns:
                        col_name = str(col).lower()
                        if "điểm" in col_name or "diem" in col_name:
                            score_col = col
                            break
                # Nếu vẫn không xác định được, mặc định cột cuối cùng là điểm
                if score_col is None:
                    score_col = df.columns[-1]
                # Nếu chưa xác định cột đơn vị, lấy cột dạng chuỗi đầu tiên (bỏ qua cột STT nếu có)
                if unit_col is None:
                    # Giả định: cột đầu có thể là STT (số), cột thứ hai là tên đơn vị
                    if len(df.columns) > 1 and pd.api.types.is_numeric_dtype(df[df.columns[0]]):
                        unit_col = df.columns[1]
                    else:
                        unit_col = df.columns[0]
                # Lấy tên kỳ (year) từ tên sheet (loại bỏ khoảng trắng)
                year = str(sheet_name).strip()
                # Tạo danh sách kết quả cho kỳ này
                entries = []
                for _, row in df.iterrows():
                    name = row[unit_col]
                    score = row[score_col]
                    if pd.isna(name) or pd.isna(score):
                        continue
                    entries.append({
                        "unit": str(name).strip(),
                        "score": float(score)
                    })
                # Sắp xếp theo điểm giảm dần và gán thứ hạng
                entries.sort(key=lambda x: x["score"], reverse=True)
                for rank, entry in enumerate(entries, start=1):
                    entry["rank"] = rank
                # Lưu dữ liệu vào cấu trúc self.data
                if idx_key not in self.data:
                    self.data[idx_key] = {"periods": {}}
                self.data[idx_key]["periods"][year] = entries
                # Lưu thông tin kỳ vào bảng ánh xạ và danh sách kỳ
                self.period_map[period_id] = (idx_key, year)
                self.periods_list.append({
                    "id": period_id,
                    "year": year,
                    "index": idx_key
                })
                period_id += 1

    def get_ranking(self, period_id: int):
        """Trả về danh sách xếp hạng (đơn vị, điểm, thứ hạng) cho period_id."""
        if period_id not in self.period_map:
            return None
        idx_key, year = self.period_map[period_id]
        data = self.data.get(idx_key, {})
        entries = data.get("periods", {}).get(year)
        return entries  # có thể trả về [] nếu không có dữ liệu

    def get_periods_by_index(self, index_id: str):
        """Trả về danh sách các kỳ (năm) cho một bộ chỉ số (theo index_id)."""
        periods = [p for p in self.periods_list if p["index"] == index_id]
        # Sắp xếp danh sách kỳ theo năm giảm dần (nếu năm là số)
        try:
            periods.sort(key=lambda x: int(x["year"]), reverse=True)
        except:
            periods.sort(key=lambda x: x["year"], reverse=True)
        # Chỉ trả về id và year (năm) cho gọn
        return [{"id": p["id"], "year": p["year"]} for p in periods]

    def get_all_periods(self):
        """Trả về danh sách tất cả các kỳ, bao gồm thông tin bộ chỉ số."""
        result = []
        for p in self.periods_list:
            idx_key = p["index"]
            idx_name = self.index_info.get(idx_key, {}).get("name", idx_key)
            result.append({
                "id": p["id"],
                "year": p["year"],
                "index": idx_key,
                "index_name": idx_name
            })
        return result

# Khởi tạo data_store toàn cục khi import module
data_store = DataStore()

def get_db():
    """Hàm dependency trả về đối tượng data_store để truy xuất dữ liệu."""
    return data_store
