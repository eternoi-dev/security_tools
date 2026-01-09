import streamlit as st
import hashlib

st.title("#️⃣ Integrity Checker (完全性確認)", anchor=False)
st.markdown("データのハッシュ値を計算し、改ざんや破損がないかを確認します。")

tab1, tab2 = st.tabs(["テキストから計算", "ファイルから計算"])

# 1. ハッシュ計算(text)
with tab1:
    st.subheader("テキストのハッシュ値を計算", anchor=False)
    input_text = st.text_area("ハッシュ化したいテキストを入力してください")
    
    if st.button("計算する", key="btn_text"):
        if input_text:
            text_bytes = input_text.encode('utf-8')
            
            md5_hash = hashlib.md5(text_bytes).hexdigest()
            sha256_hash = hashlib.sha256(text_bytes).hexdigest()
            
            st.success("計算完了")
            st.write("---")
            st.text_input("MD5 (非推奨)", md5_hash)
            st.text_input("SHA-256 (推奨)", sha256_hash)
        else:
            st.warning("テキストを入力してください。")

# 2. ハッシュ計算(file)
with tab2:
    st.subheader("ファイルのハッシュ値を計算", anchor=False)
    uploaded_file = st.file_uploader("ファイルをアップロードしてください")
    
    if st.button("計算する", key="btn_file"):
        if uploaded_file is not None:
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()
            
            file_md5 = hashlib.md5(file_bytes).hexdigest()
            file_sha256 = hashlib.sha256(file_bytes).hexdigest()
            
            st.success(f"ファイル名: {uploaded_file.name} / サイズ: {len(file_bytes)} bytes")
            st.write("---")
            st.text_input("MD5 (非推奨)", file_md5)
            st.text_input("SHA-256 (推奨)", file_sha256)
        else:
            st.warning("ファイルをアップロードしてください。")

# フッターエリア
st.markdown("---")
st.caption("© 2025 Security Engineer Portfolio Demo | Created by eternoi-dev")