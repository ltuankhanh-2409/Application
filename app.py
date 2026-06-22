import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quản lý Sinh viên", layout="centered")

st.title("🎓 Quản lý Sinh viên")

if 'sinh_vien' not in st.session_state:
    st.session_state.sinh_vien = pd.DataFrame(columns=["Mã SV", "Tên SV", "Lớp"])

with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        mssv = st.text_input("Mã sinh viên")
    with col2:
        ten = st.text_input("Tên sinh viên")
    lop = st.text_input("Lớp")
    
    submitted = st.form_submit_button("Thêm vào danh sách")
    
    if submitted:
        if mssv and ten:
            new_data = pd.DataFrame([[mssv, ten, lop]], columns=["Mã SV", "Tên SV", "Lớp"])
            st.session_state.sinh_vien = pd.concat([st.session_state.sinh_vien, new_data], ignore_index=True)
            st.success(f"Đã thêm: {ten}")

st.subheader("Danh sách sinh viên hiện tại")
st.table(st.session_state.sinh_vien)
