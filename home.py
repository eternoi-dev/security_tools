import streamlit as st

st.set_page_config(
    page_title="Security Tools",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Security Engineer Portfolio")
st.markdown("### SecOps Engine & Diagnostic Tools")

col1, col2 = st.columns([2, 1])

# 左側のカラム
with col1:
    st.info("実務における認証管理・脆弱性診断に加え、最新の脅威トレンド分析を支援するエンジニア向けツールキットです。")
    
    st.markdown("""
    #### 収録ツール一覧
    
    **01. Password Security**
    * `secrets`モジュールを用いた暗号学的安全性の確保
    * 正規表現エンジンによる複雑性ポリシーのリアルタイム検証
    
    **02. Integrity Checker**
    * 各種ハッシュアルゴリズム（SHA-256等）によるデータの完全性確認
    * クライアントサイド処理によるデータ秘匿性の維持
    
    **03. Network Recon**
    * HTTPレスポンスヘッダーの解析とセキュリティ不備の検出
    * `requests`ライブラリによる外部通信と例外ハンドリングの実装
                
    **04. Security News**
    * JVN iPedia RSSフィードの解析と、テキストマイニングによるトレンド抽出
    * `Altair`および`Pandas`を用いた頻出単語の可視化とフィルタリング
    """)

# 右側のカラム
with col2:
    st.markdown("### 👨‍💻 Author")
    st.write("作成者: eternoi-dev")
    st.write("使用技術: Python, Streamlit, Pandas, Altair, BeautifulSoup4, Requests, Regex, Secrets, Hashlib")
    
    
    st.link_button("GitHub: eternoi-dev", "https://github.com/eternoi-dev")

# フッターエリア
st.markdown("---")
st.caption("© 2025 Security Engineer Portfolio Demo | Created by eternoi-dev")