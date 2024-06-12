import streamlit as st

# تحميل الملف
file_path = "D:\Taskes\IR\Final Project\documents\document2.pdf"  # يجب تعديل هذا المسار إلى مسار الملف الخاص بك

# عرض الملف
with open(file_path, "rb") as file:
    file_bytes = file.read()

# إضافة الملف للتطبيق
st.download_button(
    label="Document2",
    data=file_bytes,
    file_name="file.pdf",  # يجب تعديل امتداد الملف هنا بناءً على نوع الملف الخاص بك
    mime="application/octet-stream"
)

