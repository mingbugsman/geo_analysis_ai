import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor
import constants as c


def train_advanced_model(df: pd.DataFrame):
    """
    Huấn luyện mô hình cực mạnh + tính toán Cooling Efficiency Score cho từng điểm
    Trả về: model, score, feature_importances_dict, cooling_potential_df
    """
    # Features
    X = df[[c.COL_LON, c.COL_LAT, c.COL_NDVI, c.COL_TDVI]]
    y = df[c.COL_TEMP]

    # Mô hình mạnh hơn RandomForest
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        subsample=0.8
    )
    model.fit(X, y)

    # Độ chính xác
    score = model.score(X, y)

    # Feature importance
    feat_names = ['Kinh độ', 'Vĩ độ', 'NDVI', 'TDVI']
    importances = dict(zip(feat_names, model.feature_importances_))

    # === TÍNH TOÁN HIỆU QUẢ LÀM MÁT CHO TỪNG ĐIỂM ===
    df_copy = df.copy()

    # Giả lập NDVI tối ưu = 0.8 (mức xanh lý tưởng), TDVI không vượt quá 0.9
    X_optimal = df_copy[[c.COL_LON, c.COL_LAT]].copy()
    X_optimal[c.COL_NDVI] = 0.80
    X_optimal[c.COL_TDVI] = df_copy[c.COL_TDVI].clip(upper=0.90)

    pred_optimal = model.predict(X_optimal)

    df_copy['Potential_Cooling'] = df_copy[c.COL_TEMP] - pred_optimal
    df_copy['Cooling_Efficiency_Score'] = (
        df_copy['Potential_Cooling'] * (1 - df_copy[c.COL_NDVI]) * 100
    ).round(2)

    # Top 500 điểm cần can thiệp nhất
    cooling_potential_df = df_copy.nlargest(500, 'Cooling_Efficiency_Score')[
        [c.COL_LAT, c.COL_LON, c.COL_TEMP, c.COL_NDVI, c.COL_TDVI,
         'Potential_Cooling', 'Cooling_Efficiency_Score']
    ].reset_index(drop=True)

    return model, score, importances, cooling_potential_df


def predict_scenario(model, df_base: pd.DataFrame, ndvi_target=0.7, tdvi_target=0.7, area_percent=100):
    """
    Dự báo kịch bản: Tăng NDVI/TDVI trên X% diện tích nóng nhất
    Trả về: giảm trung bình, giảm tối đa, số điểm được can thiệp
    """
    df = df_base.copy()

    # Ưu tiên can thiệp điểm nóng + ít cây nhất
    if 'Cooling_Efficiency_Score' in df.columns:
        df = df.sort_values('Cooling_Efficiency_Score', ascending=False)
    else:
        df = df.sort_values(c.COL_TEMP, ascending=False)

    n_points = int(len(df) * area_percent / 100)
    target_df = df.head(n_points)

    X_scenario = target_df[[c.COL_LON, c.COL_LAT]].copy()
    X_scenario[c.COL_NDVI] = ndvi_target
    X_scenario[c.COL_TDVI] = tdvi_target

    pred_new = model.predict(X_scenario)

    avg_reduction = (target_df[c.COL_TEMP].mean() - pred_new.mean())
    max_reduction = (target_df[c.COL_TEMP].max() - pred_new.min())

    return round(avg_reduction, 2), round(max_reduction, 2), len(target_df)