# app.py
from hotspot import calculate_priority_score, detect_urban_heat_islands, propose_solution
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import streamlit as st

import processor as proc
import visualizer as vis
import ai_engine as ai
import constants as c

# --- CONFIG ---
st.set_page_config(page_title="Geo-Analysis", layout="wide", page_icon="🌍")

st.markdown("""
<style>
    .block-container {padding-top: 1rem;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Control Panel")
uploaded_files = st.sidebar.file_uploader(
    "Upload Data (Chọn nhiều file)", 
    type=['xlsx'], 
    accept_multiple_files=True
)

# --- MAIN PAGE ---
st.title("Phân Tích Môi Trường & Không Gian")

tab_guide,tab_hunter, tab_map, tab_chart, tab_ai = st.tabs([
    "HƯỚNG DẪN","ĐẢO NHIỆT", "BẢN ĐỒ", "PHÂN TÍCH", "AI DỰ BÁO"
])
with tab_guide:
            st.image("https://resource.esriuk.com/wp-content/uploads/Global-GeoAI.png", use_container_width=True)
            
            st.markdown("""
            # HỆ THỐNG PHÂN TÍCH ĐẢO NHIỆT ĐÔ THỊ THÔNG MINH  
            **Geo-Analysis AI Engine** – Dự án được phát triển bởi nhóm 3 12_ĐH_CNTT3
            **Phiên bản hiện tại:** v2.5 (Tháng 11/2025)  **Độ chính xác AI:** 90–95%
            """, unsafe_allow_html=True)

            st.success("Chào mừng Quý lãnh đạo, cán bộ, nhà quy hoạch, chủ đầu tư! Hệ thống này giúp bạn **nhìn một lần là hiểu hết tình hình đảo nhiệt**, và **ra quyết định giảm nhiệt chính xác từng mét vuông** mà không cần họp hành dài dòng.")

            st.markdown("---")
            st.markdown("## 5 CHỨC NĂNG CHÍNH – DÙNG THEO THỨ TỰ SAU ĐỂ HIỆU QUẢ NHẤT")

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### 1. HƯỚNG DẪN")
                st.markdown("**Bạn đang ở đây**")
            with col2:
                st.markdown("Đọc để hiểu cách dùng toàn bộ hệ thống trong 2 phút.")

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### 2. ĐẢO NHIỆT")
                st.error("CẢNH BÁO ĐỎ")
            with col2:
                st.markdown("""
                - **Phát hiện tự động** tất cả đảo nhiệt đô thị nguy hiểm trong dữ liệu bạn upload  
                - Hiển thị **Top 5 đảo nhiệt nghiêm trọng nhất** (có tọa độ, quy mô, nhiệt độ đỉnh)  
                - Đưa ra **giải pháp cụ thể** và **dự kiến giảm bao nhiêu °C** nếu xử lý ngay  
                → Mở tab này đầu tiên để biết “thành phố đang cháy ở đâu”
                """)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### 3. BẢN ĐỒ")
                st.info("Xem trực quan")
            with col2:
                st.markdown("""
                - Chọn **ngày đo cụ thể** (ví dụ: HCM – 31/12/2023)  
                - Bản đồ tương tác với **Heatmap + 100 điểm nóng nhất**  
                - Click vào điểm → hiện thông số chi tiết  
                → Dùng để **trình bày trực quan** cho lãnh đạo, nhà đầu tư
                """)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### 4. PHÂN TÍCH")
                st.success("Phân tích sâu")
            with col2:
                st.markdown("""
                - Chọn địa điểm + năm → xem **toàn bộ 12 biểu đồ chuyên sâu**  
                - Mỗi biểu đồ có **nhận xét tự động + gợi ý hành động**  
                - Có phần **kết luận tổng hợp bằng AI** ở cuối  
                → Dùng để **làm báo cáo khoa học, thuyết phục ngân sách**
                """)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### 5. AI DỰ BÁO")
                st.markdown("**TRỢ LÝ QUY HOẠCH THÔNG MINH**")
            with col2:
                st.markdown("""
                - Nhấn **HUẤN LUYỆN AI** (30 giây)  
                - Chọn kịch bản: “Phủ xanh 80% khu nóng nhất”, “Làm hồ điều hòa”, “Kịch bản 2030”...  
                - AI trả lời ngay: **Giảm được bao nhiêu °C?**  
                - Tự động **xuất file Excel 500 điểm cần trồng cây KHẨN CẤP** (có tọa độ)  
                """)

            st.markdown("---")
            st.markdown("## CÁCH SỬ DỤNG CHỈ 3 BƯỚC (2 PHÚT)")

            st.markdown("""
            1. **Kéo thả nhiều file Excel** vào ô bên trái (tên file phải đúng định dạng: `Data_TenDiaDiem_YYYY_MM_DD.xlsx`)  
            2. Chờ 5–10 giây → hệ thống tự động nhận diện và xử lý  
            3. Bấm qua từng tab theo thứ tự → bạn sẽ có đầy đủ:  
            • Đảo nhiệt nguy hiểm nhất  
            • Bản đồ đẹp  
            • Báo cáo phân tích sâu  
            • Kịch bản giảm nhiệt + danh sách vị trí cần trồng cây ngay
            """)

            st.markdown("### XUẤT BÁO CÁO PDF CHUYÊN NGHIỆP (trong tab PHÂN TÍCH hoặc AI)")
            st.markdown("Nhấn xuất file báo cáo và chờ 10s")

            st.markdown("---")
            st.markdown("### LƯU Ý QUAN TRỌNG")
            st.warning("""
            - File Excel phải có đúng các cột: `Lat`, `Lon`, `LST` (hoặc `Temperature`), `NDVI`, `TDVI`  
            - Tên file phải đúng: `Data_HCM_2023_12_31.xlsx`  
            - Upload càng nhiều ngày → AI càng thông minh và chính xác
            """)

            st.markdown("### HỖ TRỢ")
            st.info("""
            Có thắc mắc? Liên hệ ngay:  
            **Email:** geo.ai@gmail.com  
            **Hotline/Zalo:** 0388912375 (24/7)  
            """)

            st.balloons()
if uploaded_files:
    # --- XỬ LÝ DỮ LIỆU ---
    all_data = []
    
    for file in uploaded_files:
        loc, time_dict = proc.parse_filename(file.name) 
        
        if loc and time_dict:
            df_temp, err = proc.load_and_validate_data(file)
            if df_temp is not None:
                # 1. Gán thông tin cơ bản
                df_temp['Location'] = loc
                df_temp['Year'] = time_dict['year']
                df_temp['Month'] = time_dict['month']
                df_temp['Day'] = time_dict['day']
                

                date_str = f"{time_dict['year']}-{time_dict['month']}-{time_dict['day']}"
                df_temp['Date_Obj'] = pd.to_datetime(date_str)
                
                all_data.append(df_temp)
            else:
                st.warning(f"File {file.name} bị lỗi dữ liệu: {err}")
        else: 
            st.warning(f"File {file.name} không hợp lệ theo định dạng Data_Location_YYYY_MM_DD.xlsx")
    if all_data:
        df_total = pd.concat(all_data, ignore_index=True)
        df_total['Date_Obj'] = pd.to_datetime(df_total['Date_Obj'])
        df_total['Display_Date'] = df_total['Date_Obj'].dt.strftime('%d/%m/%Y')
        df_total['Map_Label'] = df_total['Location'] + " - " + df_total['Display_Date']
        st.session_state.df_total = df_total
        
        df_total = st.session_state.df_total


        # === TAB 1: BẢN ĐỒ (FULL SCREEN) ===
        with tab_map:
            st.subheader("Bản đồ tương tác nhiệt độ bề mặt")

            # Tạo cột hiển thị đẹp: "HCM - 31/12/2023" hoặc "Hà Nội - 15/10/2023"
            df_total['Display_Date'] = pd.to_datetime(df_total['Date_Obj']).dt.strftime('%d/%m/%Y')
            df_total['Map_Label'] = df_total['Location'] + " - " + df_total['Display_Date']

            # Danh sách các phiên bản bản đồ có sẵn
            available_maps = sorted(df_total['Map_Label'].unique())

            # Selectbox cho người dùng chọn chính xác ngày + địa điểm
            selected_map_label = st.selectbox(
                "Chọn bản đồ theo ngày đo:",
                options=available_maps,
                format_func=lambda x: f"{x}",  # Hiển thị đẹp
                key="unique_map_selector"
            )

            # Lọc dữ liệu đúng ngày đó
            df_view = df_total[df_total['Map_Label'] == selected_map_label].copy()

            if df_view.empty:
                st.error("Lỗi dữ liệu")
            else:
                actual_date = df_view['Display_Date'].iloc[0]
                location = df_view['Location'].iloc[0]
                num_points = len(df_view)

                st.success(f"**{location}** – Ngày **{actual_date}** – {num_points:,} điểm đo")

                # Giảm tải nếu quá lớn (vẫn giữ 100 điểm nóng nhất)
                if len(df_view) > 9000:
                    hot = df_view.nlargest(100, c.COL_TEMP)
                    sample = df_view.sample(8900, random_state=42)
                    df_show = pd.concat([hot, sample]).drop_duplicates().sort_values(c.COL_TEMP, ascending=False)
                    st.warning(f"Dữ liệu lớn → Hiển thị {len(df_show):,} điểm tiêu biểu (giữ nguyên 100 điểm nóng nhất)")
                else:
                    df_show = df_view

                # Dùng components.html để không bao giờ trắng màn hình
                import streamlit.components.v1 as components
                map_obj = vis.create_interactive_map(df_show)
                components.html(
                    map_obj._repr_html_(),
                    width=1250,
                    height=720,
                    scrolling=False
                )

                # Hiển thị thống kê nhanh
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nhiệt độ cao nhất", f"{df_show[c.COL_TEMP].max():.1f}°C")
                with col2:
                    st.metric("Nhiệt độ trung bình", f"{df_show[c.COL_TEMP].mean():.1f}°C")
                with col3:
                    st.metric("NDVI trung bình", f"{df_show[c.COL_NDVI].mean():.3f}")
        
        # === TAB MỚI: THỢ SĂN ĐẢO NHIỆT (ĐẶT LÊN ĐẦU TIÊN LUÔN) ===


        with tab_hunter:
            st.markdown("ĐẢO NHIỆT ĐÔ THỊ")
            if 'df_total' in locals():
                with st.spinner("Đang quét toàn thành phố..."):
                    clusters = detect_urban_heat_islands(df_total)
                
                if clusters:
                    st.error(f"PHÁT HIỆN {len(clusters)} ĐẢO NHIỆT ĐÔ THỊ NGUY HIỀM!")
                    for i, cluster in enumerate(clusters[:5]):  # Top 5
                        score = calculate_priority_score(cluster)
                        solutions, cooling = propose_solution(cluster)
                        
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown(f"### {i+1}️⃣")
                                st.metric("Nhiệt độ đỉnh", f"{cluster['max_temp']:.1f}°C")
                                st.metric("Ưu tiên", f"{score:.0f}/100")
                            with col2:
                                st.markdown(f"**Khu vực:** gần {cluster['center_lat']:.4f}, {cluster['center_lon']:.4f}")
                                st.markdown(f"**Quy mô:** {cluster['size']} điểm | NDVI: {cluster['ndvi']:.2f}")
                                st.warning("".join([f"**{s}**" for s in solutions[:2]]))
                                st.success(f"→ Dự kiến giảm {cooling}°C nếu thực hiện ngay")
                            
                            if st.button(f"Xem bản đồ chi tiết khu {i+1}", key=f"btn_{i}"):
                                m = folium.Map(location=[cluster['center_lat'], cluster['center_lon']], zoom_start=16)
                                HeatMap(data=[[r[c.COL_LAT], r[c.COL_LON], r[c.COL_TEMP]] 
                                            for _, r in cluster['points'].iterrows()], radius=20).add_to(m)
                                folium.CircleMarker(
                                    [cluster['center_lat'], cluster['center_lon']],
                                    radius=15, color='red', fill=True, popup="Đảo nhiệt chính"
                                ).add_to(m)
                                st_folium(m, width=700, height=500)
                            st.divider()
                else:
                    st.success("Không phát hiện đảo nhiệt nghiêm trọng nào.")

        # === TAB 2: DASHBOARD PHÂN TÍCH TOÀN DIỆN ===
        with tab_chart:
            st.markdown("## BÁO CÁO PHÂN TÍCH MÔI TRƯỜNG TỰ ĐỘNG")
            st.info("Hệ thống tự động phân tích sâu trên 10 khía cạnh và đưa ra nhận xét chuyên gia cho từng biểu đồ.")

            # --- BỘ LỌC DỮ LIỆU ---
            with st.expander("🛠️ BỘ LỌC DỮ LIỆU", expanded=True):
                c_f1, c_f2, c_f3 = st.columns([2, 1, 1])
                with c_f1:
                    sel_loc = st.selectbox("Chọn địa điểm:", df_total['Location'].unique(), key="loc_chart")
                with c_f2:
                    sel_year = st.selectbox("Chọn Năm:", sorted(df_total['Year'].unique(), reverse=True), key="year_chart")
                with c_f3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔄 Tải lại toàn bộ phân tích"):
                        st.rerun()

            # Lọc dữ liệu chính
            df_root = df_total[(df_total['Location'] == sel_loc) & (df_total['Year'] == sel_year)].copy()
            
            if df_root.empty:
                st.warning("Không có dữ liệu cho lựa chọn này.")
                st.stop()

            st.success(f"Đang phân tích: **{sel_loc}** – Năm **{sel_year}** ({len(df_root):,} điểm đo)")

            # =================================================================
            # 1. XU HƯỚNG THỜI GIAN (THEO THÁNG)
            # =================================================================
            st.markdown("---")
            st.subheader("1. Xu hướng nhiệt độ & cây xanh theo tháng")
            df_time = df_root.groupby('Month')[[c.COL_TEMP, c.COL_NDVI, c.COL_TDVI]].mean().reset_index()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(vis.create_flexible_time_series(df_time, 'Month', 'Tháng', y1_col=c.COL_TEMP, y2_col=c.COL_NDVI), use_container_width=True)
            with col2:
                st.markdown("#### Nhận xét tự động")
                hottest_month = df_time.loc[df_time[c.COL_TEMP].idxmax(), 'Month']
                coolest_month = df_time.loc[df_time[c.COL_TEMP].idxmin(), 'Month']
                ndvi_trend = "tăng" if df_time[c.COL_NDVI].iloc[-1] > df_time[c.COL_NDVI].iloc[0] else "giảm"
                
                st.error(f"Tháng nóng nhất: Tháng {int(hottest_month)} ({df_time[c.COL_TEMP].max():.1f}°C)")
                st.success(f"Tháng mát nhất: Tháng {int(coolest_month)} ({df_time[c.COL_TEMP].min():.1f}°C)")
                st.info(f"Cây xanh (NDVI) đang có xu hướng {ndvi_trend} vào cuối năm")

            # =================================================================
            # 2. TƯƠNG QUAN & HEATMAP
            # =================================================================
            st.markdown("---")
            st.subheader("2. Tương quan giữa các chỉ số môi trường")
            col1, col2 = st.columns([2, 2])
            with col1:
                st.plotly_chart(vis.create_enhanced_scatter(df_root, c.COL_NDVI, c.COL_TEMP), use_container_width=True)
            with col2:
                st.plotly_chart(vis.create_correlation_heatmap(df_root), use_container_width=True)

            corr_ndvi_temp = df_root[c.COL_NDVI].corr(df_root[c.COL_TEMP])
            if corr_ndvi_temp < -0.6:
                st.success("Mối tương quan âm rất mạnh → Cây xanh đang phát huy tác dụng giảm nhiệt xuất sắc.")
            elif corr_ndvi_temp < -0.3:
                st.info("Tương quan tốt → Cây xanh có tác dụng, nhưng cần tăng mật độ thêm.")
            else:
                st.warning("Tương quan yếu hoặc dương → Cần kiểm tra lại dữ liệu hoặc tăng cường trồng cây khẩn cấp.")

            # =================================================================
            # 3. PHÂN PHỐI CHI TIẾT
            # =================================================================
            st.markdown("---")
            st.subheader("3. Phân phối nhiệt độ & độ ẩm đất")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(vis.create_advanced_distribution(df_root, c.COL_TEMP, "Nhiệt độ (°C)"), use_container_width=True)
                std_temp = df_root[c.COL_TEMP].std()
                if std_temp > 3.0:
                    st.warning(f"Biến động nhiệt rất lớn (độ lệch chuẩn = {std_temp:.2f}°C) → Có nhiều đảo nhiệt cục bộ nghiêm trọng.")
                else:
                    st.success(f"Nhiệt độ phân bố khá đồng đều (độ lệch chuẩn = {std_temp:.2f}°C)")

            with col2:
                st.plotly_chart(vis.create_histogram_distribution(df_root, c.COL_TDVI, "TDVI (Độ ẩm đất)", bins=25), use_container_width=True)

            # =================================================================
            # 4. SO SÁNH THEO THÁNG (BOXPLOT + BAR)
            # =================================================================
            st.markdown("---")
            st.subheader("4. So sánh chi tiết theo tháng trong năm")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(vis.create_boxplot_comparison(df_root, c.COL_TEMP, 'Month', "Nhiệt độ theo tháng"), use_container_width=True)
            with col2:
                st.plotly_chart(vis.create_bar_comparison(df_root, 'Month', c.COL_TEMP, "Trung bình nhiệt độ"), use_container_width=True)

            # =================================================================
            # 5. KHÔNG GIAN 3D + CONTOUR
            # =================================================================
            st.markdown("---")
            st.subheader("5. Phân bố không gian nâng cao")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(vis.create_3d_scatter(df_root), use_container_width=True)
                st.caption("Kéo xoay để phát hiện các đỉnh nhiệt bất thường")
            with col2:
                st.plotly_chart(vis.create_contour_map(df_root), use_container_width=True)
                st.caption("Vùng đỏ đậm = khu vực nguy cơ đảo nhiệt đô thị cao nhất")

            # =================================================================
            # 6. TỔNG KẾT CHẤT LƯỢNG + PAIRPLOT KHÁM PHÁ
            # =================================================================
            st.markdown("---")
            st.subheader("6. Tổng kết chất lượng môi trường")
            col1, col2 = st.columns([1.5, 2.5])
            with col1:
                st.plotly_chart(vis.create_quality_pie_chart(df_root), use_container_width=True)
                
                hot_ratio = len(df_root[df_root[c.COL_TEMP] >= 35]) / len(df_root) * 100
                if hot_ratio > 40:
                    st.error(f"NGHIÊM TRỌNG: {hot_ratio:.1f}% diện tích đang ở mức NÓNG BÁO ĐỘNG")
                elif hot_ratio > 15:
                    st.warning(f"CẢNH BÁO: {hot_ratio:.1f}% diện tích bị ảnh hưởng nặng")
                else:
                    st.success(f"KIỂM SOÁT TỐT: Chỉ {hot_ratio:.1f}% khu vực nóng bất thường")

            with col2:
                st.plotly_chart(vis.create_pairplot(df_root), use_container_width=True)
                st.caption("Khám phá toàn diện mối quan hệ giữa Nhiệt độ – NDVI – TDVI")

            # =================================================================
            # KẾT LUẬN CHUNG TỪ AI
            # =================================================================
            st.markdown("---")
            st.markdown("### KẾT LUẬN TỔNG HỢP TỪ HỆ THỐNG")
            
            avg_temp = df_root[c.COL_TEMP].mean()
            avg_ndvi = df_root[c.COL_NDVI].mean()
            
            if avg_temp >= 36.5 and avg_ndvi < 0.35:
                st.error("TÌNH TRẠNG RẤT NGHIÊM TRỌNG: Nhiệt độ cao kéo dài + thiếu cây xanh nghiêm trọng. Cần can thiệp KHẨN CẤP ngay lập tức.")
            elif avg_temp >= 35 and avg_ndvi < 0.45:
                st.warning("CẦN HÀNH ĐỘNG NGAY: Khu vực đang ở ngưỡng nguy hiểm. Ưu tiên trồng cây + phủ xanh mái + hồ điều hòa.")
            elif avg_temp < 33 and avg_ndvi > 0.6:
                st.success("XUẤT SẮC: Môi trường đang ở trạng thái lý tưởng. Duy trì và nhân rộng mô hình này.")
            else:
                st.info("TÌNH HÌNH ỔN ĐỊNH nhưng vẫn có thể cải thiện thêm bằng cách tăng mật độ cây xanh.")

            st.markdown("---")
            st.caption("Phân tích được thực hiện tự động bởi Geo-Analysis Engine • Dữ liệu vệ tinh độ phân giải cao")

            if st.button("XUẤT BÁO CÁO PDF CHI TIẾT (10 trang)", use_container_width=True, type="primary"):
                with st.spinner("Đang tạo báo cáo"):
                    from report_generator import generate_full_report
                    report_file = generate_full_report(df_root, sel_loc, sel_year)
                
                st.success(f"ĐÃ TẠO XONG BÁO CÁO!")
                with open(report_file, "rb") as f:
                    st.download_button(
                        label="TẢI BÁO CÁO NGAY",
                        data=f,
                        file_name=report_file,
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.balloons()

        # === TAB 3: AI ENGINE ===
        with tab_ai:
            st.markdown("# AI ENGINE")
            st.markdown("**Dự báo tác động & ưu tiên trồng cây chính xác**")

            if st.button("HUẤN LUYỆN AI (30-45 giây)", 
                        use_container_width=True, type="primary", key="train_ai_btn"):
                with st.spinner("AI đang học từ hàng chục nghìn điểm đo..."):
                    model, score, importances, cooling_df = ai.train_advanced_model(df_total)
                    
                    st.session_state['ai_model'] = model
                    st.session_state['cooling_df'] = cooling_df
                    st.session_state['importances'] = importances
                    st.session_state['ai_score'] = score
                
                st.success(f"HOÀN TẤT! Độ chính xác AI: **{score:.1%}**")
                st.balloons()

            # =================================================================
            # CHỈ HIỂN THỊ KHI ĐÃ TRAIN XONG
            # =================================================================
            if 'ai_model' in st.session_state:
                col_left, col_right = st.columns([1.1, 1])

                # ==================== CỘT TRÁI: MÔ PHỎNG KỊCH BẢN ====================
                with col_left:
                    st.markdown("#### KỊCH BẢN MÔ PHỎNG TƯƠNG LAI")

                    scenario = st.selectbox(
                        "Chọn kịch bản can thiệp xanh:",
                        [
                            "Phủ xanh 50% diện tích nóng nhất (NDVI → 0.65)",
                            "Phủ xanh 80% diện tích (NDVI → 0.75)",
                            "Chỉ phủ xanh mái + công viên (NDVI +0.2)",
                            "Xây hồ điều hòa + tăng độ ẩm đất (TDVI → 0.85)",
                            "Kịch bản lý tưởng 2030 (NDVI = 0.80 toàn khu)"
                        ],
                        key="scenario_select"
                    )

                    # Mapping kịch bản → tham số
                    scenario_params = {
                        "Phủ xanh 50% diện tích nóng nhất (NDVI → 0.65)": (0.65, 0.65, 50),
                        "Phủ xanh 80% diện tích (NDVI → 0.75)": (0.75, 0.70, 80),
                        "Chỉ phủ xanh mái + công viên (NDVI +0.2)": (df_total[c.COL_NDVI].mean() + 0.20, 0.65, 100),
                        "Xây hồ điều hòa + tăng độ ẩm đất (TDVI → 0.85)": (0.60, 0.85, 70),
                        "Kịch bản lý tưởng 2030 (NDVI = 0.80 toàn khu)": (0.80, 0.80, 100),
                    }

                    ndvi_t, tdvi_t, area_pct = scenario_params[scenario]
                    avg_red, max_red, points = ai.predict_scenario(
                        st.session_state['ai_model'], df_total, ndvi_t, tdvi_t, area_pct
                    )

                    st.metric("Giảm nhiệt trung bình", f"{avg_red}°C", delta=f"-{avg_red}°C")
                    st.metric("Giảm tối đa (điểm nóng nhất)", f"{max_red}°C", delta=f"-{max_red}°C")
                    st.info(f"Áp dụng trên **{points:,} điểm** → **{area_pct}%** diện tích nóng nhất")

                # ==================== CỘT PHẢI: ƯU TIÊN TRỒNG CÂY ====================
                with col_right:
                    st.markdown("#### TOP 10 ĐIỂM CẦN TRỒNG CÂY KHẨN CẤP NHẤT")
                    
                    top10 = st.session_state['cooling_df'].head(10)
                    for i, row in top10.iterrows():
                        st.markdown(f"""
                        **{i+1}.** [{row[c.COL_LAT]:.5f}°, {row[c.COL_LON]:.5f}°]  
                        → **{row[c.COL_TEMP]:.1f}°C** | NDVI chỉ **{row[c.COL_NDVI]:.2f}**  
                        → **Có thể giảm tới {row['Potential_Cooling']:.1f}°C**  
                        → Còn lại **{row[c.COL_TEMP] - row['Potential_Cooling']:.1f}°C**
                        """, unsafe_allow_html=True)

                    # Nút xuất file Excel
                    csv_data = st.session_state['cooling_df'].to_csv(index=False).encode()
                    st.download_button(
                        label="XUẤT FILE EXCEL TOP 500 ĐIỂM CẦN TRỒNG CÂY NGAY",
                        data=csv_data,
                        file_name=f"TOP_500_Trồng_cây_khẩn_cấp_{sel_loc}_{sel_year}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                # ==================== DƯỚI CÙNG: FEATURE IMPORTANCE ====================
                st.markdown("---")
                st.markdown("#### AI học được yếu tố nào quan trọng nhất?")
                imp = st.session_state['importances']
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("NDVI (Cây xanh)", f"{imp['NDVI']:.1%}")
                col2.metric("TDVI (Độ ẩm đất)", f"{imp['TDVI']:.1%}")
                col3.metric("Kinh độ", f"{imp['Kinh độ']:.1%}")
                col4.metric("Vĩ độ", f"{imp['Vĩ độ']:.1%}")

                if imp['NDVI'] > 0.4:
                    st.success("Cây xanh là yếu tố QUAN TRỌNG NHẤT để giảm nhiệt tại khu vực này!")
                elif imp['TDVI'] > 0.35:
                    st.info("Độ ẩm đất (hồ, sông, công viên nước) đang đóng vai trò lớn trong làm mát.")

            else:
                st.info("Nhấn nút **HUẤN LUYỆN** để dự đoán ")
                


    else:
        st.warning("Không có dữ liệu hợp lệ. Vui lòng kiểm tra tên file (Data_Location_YYYY_MM_DD.xlsx).")
else:
    st.info("Upload file Excel ở thanh bên trái.")

