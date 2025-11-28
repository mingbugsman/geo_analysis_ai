# processor.py
import pandas as pd
import re
from typing import Tuple, Optional
import constants as c

def parse_filename(filename: str) -> Tuple[Optional[str], Optional[dict]]:
    """
    Phân tích tên file và trả về cả dictionary thời gian
    Output: "HCM", {'year': 2023, 'month': 12, 'day': 22}
    """
    match = re.search(c.FILE_PATTERN, filename)
    if match:
        location = match.group(1)
        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))
        return location, {'year': year, 'month': month, 'day': day}
    return None, None

def load_and_validate_data(file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Đọc file Excel và kiểm tra tính hợp lệ của dữ liệu.
    Trả về: (DataFrame, Error_Message)
    """
    try:
        df = pd.read_excel(file)
        
        # 1. Kiểm tra cột thiếu
        if not c.REQUIRED_COLUMNS.issubset(df.columns):
            missing = c.REQUIRED_COLUMNS - set(df.columns)
            return None, f"File thiếu các cột bắt buộc: {missing}"
        
       
        original_len = len(df)
        df.dropna(subset=c.REQUIRED_COLUMNS, inplace=True)
        
      
        if len(df) < original_len:
            print(f"⚠️ Đã loại bỏ {original_len - len(df)} dòng dữ liệu rỗng/lỗi.")

        if df.empty:
            return None, "File có dữ liệu nhưng toàn bộ đều chứa giá trị rỗng (NaN)."
            
        return df, None
    except Exception as e:
        return None, f"Lỗi không xác định khi đọc file: {str(e)}"