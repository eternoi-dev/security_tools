import streamlit as st
import secrets
import string
import re

st.set_page_config(page_title="Password Manager", page_icon="🔑")

st.title("🔑 Password Manager", anchor=False)
st.markdown("パスワードの強度判定と、暗号学的に安全な乱数生成を行うモジュールです。")

tab1, tab2 = st.tabs(["🛡️ 強度チェック", "🎲 パスワード生成"])

# 1. 強度判定
with tab1:
    st.subheader("パスワード脆弱性判定", anchor=False)

    password = st.text_input("判定する文字列を入力", type="password")

    if st.button("脆弱性を確認する"):
        
        if not password:
            st.warning("パスワードが入力されていません。")
        else:
            score = 0
            feedback = []

            if len(password) >= 12:
                score += 1
            else:
                feedback.append("⚠️ 文字数が不足しています（12文字以上を推奨）")

            patterns = [
                (r"[a-z]", "小文字(a-z)"),
                (r"[A-Z]", "大文字(A-Z)"),
                (r"[0-9]", "数字(0-9)"),
                (r"[!@#$%^&*]", "記号(!@#$%^&*)")
            ]

            for pattern, label in patterns:
                if re.search(pattern, password):
                    score += 1
                else:
                    feedback.append(f"⚠️ {label}が含まれていません")

            st.markdown("---")
            
            if score == 5:
                st.success("✅ 非常に強力なパスワードです")
                st.balloons()
            elif score >= 3:
                st.warning("⚠️ 標準的な強度です。改善を推奨します。")
                for f in feedback: st.write(f)
            else:
                st.error("❌ 脆弱です。直ちに変更を検討してください。")
                for f in feedback: st.write(f)

# 2. パスワード生成
with tab2:
    st.subheader("暗号学的乱数によるパスワード生成", anchor=False)
    
    length = st.slider("文字数選択", 8, 32, 16)
    use_symbol = st.checkbox("特殊記号を含める (!@#$%^&*)", value=True)

    if st.button("Generate"):
        source_chars = string.ascii_letters + string.digits
        symbols = "!@#$%^&*"
        if use_symbol:
            source_chars += symbols

        while True:
            password = ''.join(secrets.choice(source_chars) for _ in range(length))

            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            
            has_symbol = any(c in symbols for c in password) if use_symbol else True

            if has_upper and has_lower and has_digit and has_symbol:
                break

        st.success("パスワードを生成しました")
        st.code(password, language=None)
        st.caption("※secretsモジュールを使用し、複雑性要件を満たすまで再生成を行っています。")

# フッターエリア
st.markdown("---")
st.caption("© 2025 Security Engineer Portfolio Demo | Created by eternoi-dev")