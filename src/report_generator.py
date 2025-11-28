import plotly.io as pio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from io import BytesIO
from datetime import datetime
import os
import re


from visualizer import *


pio.templates.default = "plotly_white"


def clean_text_for_pdf(text):
    """Làm sạch text HTML để in lên PDF"""
    if not text: return ""
    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    text = re.sub('<[^<]+?>', '', text) # Xóa thẻ HTML
    return text.strip()

def create_report_page(pdf, fig_plotly, title, comment=None):
    """Tạo 1 trang PDF từ biểu đồ Plotly"""
    if fig_plotly is None: return
    try:
        # Xuất hình ra RAM
        img_bytes = fig_plotly.to_image(format="png", width=1200, height=700, scale=2)
        img = plt.imread(BytesIO(img_bytes))

        # Tạo trang Matplotlib
        mfig = Figure(figsize=(11.69, 8.27), dpi=150) # A4 Ngang
        ax = mfig.add_subplot(111)
        ax.imshow(img)
        ax.axis('off')

        # Header
        mfig.text(0.05, 0.95, title.upper(), fontsize=14, weight='bold', color='#1a237e')
        
        # Footer (Comment)
        if comment:
            clean_comment = clean_text_for_pdf(comment)
            mfig.text(0.05, 0.05, clean_comment, fontsize=11, family='sans-serif',
                     verticalalignment='bottom',
                     bbox=dict(boxstyle='round,pad=1', facecolor='#f1f8e9', edgecolor='#81c784'))
            mfig.subplots_adjust(bottom=0.25)
        else:
            mfig.subplots_adjust(bottom=0.05)

        pdf.savefig(mfig)
        plt.close(mfig)
        print(f"-> [OK] {title}")
    except Exception as e:
        print(f"-> [LỖI] Không thể vẽ {title}: {e}")

# --- HÀM CHÍNH ---
def generate_full_report(df_root, location="Không xác định", year=None):
    """
    Xuất báo cáo PDF chứa ĐẦY ĐỦ mọi biểu đồ trong Visualizer
    """
    # 1. Setup tên file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    os.makedirs("../reports", exist_ok=True)
    pdf_name = f"reports/FULL_REPORT_{location}_{timestamp}.pdf"
    html_name = f"reports/MAP_{location}_{timestamp}.html"

    print(f"--- BẮT ĐẦU TẠO BÁO CÁO FULL ---")
    
    # Chuẩn bị dữ liệu phụ trợ (Group by Month)
    df_month = df_root.groupby('Month')[[c.COL_TEMP, c.COL_NDVI, c.COL_TDVI]].mean().reset_index()

    with PdfPages(pdf_name) as pdf:
        
        # === TRANG BÌA ===
        mfig = Figure(figsize=(11.69, 8.27))
        ax = mfig.add_subplot(111)
        ax.axis('off')
        mfig.text(0.5, 0.6, "BÁO CÁO PHÂN TÍCH TOÀN DIỆN\n(FULL ANALYTICAL REPORT)", 
                 ha='center', fontsize=24, weight='bold', color='#b71c1c')
        mfig.text(0.5, 0.4, f"Khu vực: {location}\nSố lượng biểu đồ: 12 + 1 Bản đồ số", ha='center', fontsize=14)
        pdf.savefig(mfig)
        plt.close(mfig)

        # === NHÓM 1: BIẾN ĐỘNG THỜI GIAN (TEMPORAL) ===
        
        # 1. Time Series (Temp + NDVI)
        fig1 = create_flexible_time_series(df_month, 'Month', 'Tháng')
        create_report_page(pdf, fig1, "1. Diễn biến Nhiệt độ & Cây xanh (Time Series)", 
                           "So sánh trực quan sự thay đổi của Nhiệt độ và thảm thực vật theo thời gian.")

        # 13. Time Series (TDVI)
        fig13 = create_tdvi_time_series(df_month, 'Month', 'Tháng')
        create_report_page(pdf, fig13, "2. Biến động Độ ẩm đất (TDVI)", 
                           "Theo dõi nguy cơ hạn hán và độ ẩm bề mặt.")

        # 12. Bar Comparison
        fig12 = create_bar_comparison(df_root, group_col='Month', label_vn="Nhiệt độ trung bình tháng")
        create_report_page(pdf, fig12, "3. So sánh Nhiệt độ Trung bình Tháng", 
                           "Nhận diện tháng nóng nhất trong năm (Bar Chart).")

        # === NHÓM 2: TƯƠNG QUAN & NGUYÊN NHÂN (CORRELATION) ===

        # 2. Scatter Plot
        fig2 = create_enhanced_scatter(df_root)
        create_report_page(pdf, fig2, "4. Tương quan Hồi quy (Scatter Plot)", 
                           "Đánh giá hiệu quả làm mát của cây xanh: Đường đỏ đi xuống là Tốt.")

        # 7. Heatmap Matrix
        fig7 = create_correlation_heatmap(df_root)
        create_report_page(pdf, fig7, "5. Ma trận Tương quan (Heatmap)", 
                           "Tổng hợp mức độ ảnh hưởng lẫn nhau giữa tất cả các chỉ số.")

        # 11. Pairplot
        # Lưu ý: Pairplot có thể vẽ hơi lâu nếu dữ liệu quá lớn
        if len(df_root) > 2000: 
            print("-> [INFO] Dữ liệu > 2000 dòng, lấy mẫu ngẫu nhiên cho Pairplot để tránh treo máy.")
            df_sample = df_root.sample(1000)
        else:
            df_sample = df_root
        fig11 = create_pairplot(df_sample)
        create_report_page(pdf, fig11, "6. Phân tích Đa biến (Pairplot)", 
                           "Khám phá các cụm dữ liệu và quan hệ chéo tổng quát.")

        # === NHÓM 3: PHÂN PHỐI & THỐNG KÊ (DISTRIBUTION) ===

        # 6. Pie Chart
        fig6 = create_quality_pie_chart(df_root)
        create_report_page(pdf, fig6, "7. Tỷ lệ Phân loại Chất lượng", 
                           "Tỷ lệ % diện tích nằm trong vùng An toàn vs Nguy hiểm.")

        # 3. Violin Plot
        fig3 = create_advanced_distribution(df_root, c.COL_TEMP, "Nhiệt độ")
        create_report_page(pdf, fig3, "8. Phân phối Mật độ Dữ liệu (Violin)", 
                           "Xem hình dáng phân phối của nhiệt độ (độ lệch chuẩn, trung vị).")

        # 8. Histogram
        fig8 = create_histogram_distribution(df_root, c.COL_TEMP, "Nhiệt độ")
        create_report_page(pdf, fig8, "9. Tần suất xuất hiện (Histogram)", 
                           "Số lượng điểm đo rơi vào từng khoảng nhiệt độ cụ thể.")

        # 9. Boxplot Comparison
        fig9 = create_boxplot_comparison(df_root, group_col='Month')
        create_report_page(pdf, fig9, "10. Biến động dải nhiệt theo nhóm (Boxplot)", 
                           "So sánh độ phân tán nhiệt độ giữa các tháng (Max, Min, Median).")

        # === NHÓM 4: KHÔNG GIAN (SPATIAL) ===

        # 10. Contour Map
        fig10 = create_contour_map(df_root)
        create_report_page(pdf, fig10, "11. Bản đồ Đường đồng mức (Contour)", 
                           "Hình dung các vòng tròn nhiệt lan tỏa từ tâm đô thị.")

        # 4. 3D Scatter
        fig4 = create_3d_scatter(df_root)
        create_report_page(pdf, fig4, "12. Mô hình Nhiệt độ 3D", 
                           "Góc nhìn 3 chiều về địa hình nhiệt độ (Kinh độ - Vĩ độ - Nhiệt độ).")

        # === TRANG CUỐI ===
        mfig = Figure(figsize=(11.69, 8.27))
        ax = mfig.add_subplot(111)
        ax.axis('off')
        ax.text(0.5, 0.5, f"KẾT THÚC BÁO CÁO\n\nLưu ý: Bản đồ tương tác (Interactive Map)\nđã được lưu riêng tại file:\n{html_name}", 
                ha='center', fontsize=16)
        pdf.savefig(mfig)
        plt.close(mfig)

    # === XỬ LÝ RIÊNG CHO BẢN ĐỒ INTERACTIVE (FOLIUM) ===
    try:
        print("-> Đang tạo bản đồ HTML (Folium)...")
        m = create_interactive_map(df_root)
        m.save(html_name)
        print(f"-> [OK] Đã lưu bản đồ: {html_name}")
    except Exception as e:
        print(f"-> [LỖI] Không thể lưu bản đồ HTML: {e}")

    print(f"\n=== HOÀN TẤT ===")
    print(f"1. PDF Report: {pdf_name}")
    print(f"2. HTML Map:   {html_name}")
    
    return pdf_name