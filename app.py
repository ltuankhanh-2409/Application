import streamlit as st
import pandas as pd
import os

# Cấu hình trang
st.set_page_config(page_title="Quản lý Chi tiêu", layout="wide")
st.title("💰 Quản lý Chi tiêu Gia đình")

DATA_FILE = "chi_tieu.csv"

# Hàm tải dữ liệu
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["ID", "Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú"])
    return pd.read_csv(DATA_FILE)

# --- KHỐI NHẬP LIỆU (THÊM) ---
with st.expander("➕ Thêm giao dịch mới"):
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        ngay = col1.date_input("Ngày giao dịch")
        loai = col2.selectbox("Loại", ["Thu nhập", "Chi tiêu"])
        danh_muc = col1.text_input("Danh mục")
        so_tien = col2.number_input("Số tiền", min_value=0, step=1000)
        ghi_chu = st.text_input("Ghi chú")
        
        if st.form_submit_button("Lưu giao dịch"):
            df = load_data()
            new_id = len(df) + 1 if df.empty else df["ID"].max() + 1
            new_row = {"ID": new_id, "Ngày": ngay, "Loại": loai, "Danh mục": danh_muc, "Số tiền": so_tien, "Ghi chú": ghi_chu}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Đã lưu!")
            st.rerun()

# --- KHỐI QUẢN TRỊ (XÓA & XUẤT EXCEL) ---
df = load_data()

col_xoa, col_excel = st.columns([1, 1])
with col_xoa:
    with st.expander("❌ Xóa giao dịch"):
        del_id = st.number_input("Nhập ID cần xóa", min_value=1, step=1)
        if st.button("Xác nhận xóa"):
            df = df[df["ID"] != del_id]
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

with col_excel:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Tải dữ liệu về Excel", csv, "chi_tieu.csv", "text/csv")

# --- HIỂN THỊ DỮ LIỆU ---
st.subheader("📋 Bảng chi tiết")
df = df.sort_values(by="Ngày", ascending=False)
st.dataframe(df, use_container_width=True)
