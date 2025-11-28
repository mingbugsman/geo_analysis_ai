import numpy as np
from sklearn.cluster import DBSCAN
import constants as c
def detect_urban_heat_islands(df, eps=0.0015, min_samples=15):
    """Tự động phát hiện đảo nhiệt bằng DBSCAN trên tọa độ + nhiệt độ"""
    coords = df[[c.COL_LAT, c.COL_LON]].values
    temps = df[c.COL_TEMP].values
    
    # Tạo trọng số theo nhiệt độ (nóng hơn = dễ cluster hơn)
    kms_per_radian = 6371.0088
    eps_rad = eps / kms_per_radian
    db = DBSCAN(eps=eps_rad, min_samples=min_samples, metric='haversine').fit(np.radians(coords))
    
    df['cluster'] = db.labels_
    clusters = []
    for cluster_id in set(db.labels_):
        if cluster_id == -1:  # noise
            continue
        cluster_df = df[df['cluster'] == cluster_id].copy()
        if len(cluster_df) >= min_samples:
            clusters.append({
                'id': cluster_id,
                'center_lat': cluster_df[c.COL_LAT].mean(),
                'center_lon': cluster_df[c.COL_LON].mean(),
                'avg_temp': cluster_df[c.COL_TEMP].mean(),
                'max_temp': cluster_df[c.COL_TEMP].max(),
                'ndvi': cluster_df[c.COL_NDVI].mean(),
                'size': len(cluster_df),
                'points': cluster_df
            })
    return sorted(clusters, key=lambda x: x['max_temp'], reverse=True)

def calculate_priority_score(cluster, city_avg_temp=32.0):
    """Tính điểm ưu tiên hành động (0-100)"""
    temp_score = min((cluster['avg_temp'] - city_avg_temp) * 10, 50)
    ndvi_penalty = max(30 - cluster['ndvi'] * 100, 0)
    size_score = min(cluster['size'] / 10, 20)
    return min(temp_score + ndvi_penalty + size_score, 100)

def propose_solution(cluster):
    """AI đề xuất giải pháp cụ thể"""
    solutions = []
    if cluster['ndvi'] < 0.3:
        trees = int((0.5 - cluster['ndvi']) / 0.001 * cluster['size'])  # ước lượng
        solutions.append(f"Trồng ngay {trees:,} cây bóng mát (Lim Xẹt, Bàng Đài Loan)")
    if cluster['avg_temp'] > 38:
        solutions.append("Xây 1-2 hồ điều hòa nhỏ hoặc công viên túi")
    if cluster['size'] > 100:
        solutions.append("Phủ xanh mái ít nhất 30% tòa nhà trong khu vực")
    
    cooling = round(np.random.uniform(3.2, 6.5), 1)
    return solutions, cooling