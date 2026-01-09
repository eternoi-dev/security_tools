import streamlit as st
import requests

st.title("🌐 Network Recon (ヘッダー診断)", anchor=False)
st.markdown("""
指定したWebサイトの **HTTPレスポンスヘッダー** を取得し、
セキュリティ対策（HSTS, CSPなど）が正しく設定されているか簡易診断します。
""")

headers_ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

default_url = "https://eternoi-security-tools.streamlit.app/"
url = st.text_input("診断したいURLを入力 (http:// or https://)", default_url)

allow_get = st.checkbox("HEADメソッドが拒否された場合、GETメソッドで再試行する", value=False, help="HEADメソッド（ヘッダー取得のみ）が禁止されているサーバーの場合、GETメソッド（通常のアクセス）で再試行します。GETの場合、レスポンスの中身もダウンロードするため通信量が増える可能性があります。")

# 1. ヘッダー診断
if st.button("診断開始", key="btn_recon"):
    if url:
        response = None
        
        try:
            try:
                with st.spinner('HEADメソッドでアクセス中...'):
                    res_head = requests.head(url, timeout=5, verify=True, allow_redirects=True, headers=headers_ua)
                
                if res_head.status_code == 405 or res_head.status_code == 403:
                    raise requests.exceptions.RequestException("HEAD method not allowed")
                
                response = res_head
                st.info("ℹ️ HEADメソッドで情報を取得しました。（安全・高速）")

            except requests.exceptions.RequestException:
                if allow_get:
                    with st.spinner('HEADが拒否されました。GETメソッドで再試行中...'):
                        response = requests.get(url, timeout=5, verify=True, allow_redirects=True, headers=headers_ua)
                    st.warning("⚠️ HEADメソッドが拒否されたため、GETメソッドで情報を取得しました。")
                else:
                    st.error("❌ HEADメソッドでのアクセスが拒否されました。")
                    st.markdown("Webサーバーの設定により、HEADリクエストが禁止されているようです。")
                    st.markdown("診断を続行するには、上の **「HEADメソッドが拒否された場合、GETメソッドで再試行する」** にチェックを入れてください。")
                    st.stop()

            if response.status_code == 200:
                st.success(f"アクセス成功: Status Code {response.status_code}")
            elif response.status_code >= 500:
                st.error(f"サーバーエラーですがヘッダーは取得しました: Status Code {response.status_code}")
            else:
                st.warning(f"アクセス成功: Status Code {response.status_code}")
            headers = response.headers
            
            st.subheader("🛡️ セキュリティヘッダー診断結果", anchor=False)
            
            security_headers = [
                "Strict-Transport-Security",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Content-Security-Policy" 
            ]
            
            for h in security_headers:
                if h in headers:
                    st.success(f"✅ {h}: 設定されています")
                    with st.expander(f"設定値を見る ({h})"):
                        st.code(headers[h])
                else:
                    st.error(f"❌ {h}: 設定されていません (推奨)")
            
            st.markdown("---")
            st.subheader("🕵️ サーバー情報の漏洩チェック", anchor=False)
            if "Server" in headers:
                st.warning(f"⚠️ Serverヘッダーが見えています: {headers['Server']}")
            else:
                st.info("✅ Serverヘッダーは隠蔽されています（Good!）")

            with st.expander("取得した全てのヘッダー情報を見る"):
                for key, value in headers.items():
                    st.markdown(f"**{key}**: `{value}`")
                    
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("URLを入力してください。")

# フッターエリア
st.markdown("---")
st.caption("© 2025 Security Engineer Portfolio Demo | Created by eternoi-dev")