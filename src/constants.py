# Định nghĩa tên các cột dữ liệu bắt buộc
COL_LAT = 'POINT_Y'
COL_LON = 'POINT_X'
COL_NDVI = 'NDVI'
COL_TDVI = 'TVDI'
COL_TEMP = 'Temperature'
# Danh sách cột bắt buộc phải có trong file Excel
REQUIRED_COLUMNS = {COL_LAT, COL_LON, COL_NDVI, COL_TDVI, COL_TEMP}

# Regex pattern để bắt tên file
FILE_PATTERN = r"Data_(.*?)_(\d{4})_(\d{1,2})_(\d{1,2})"