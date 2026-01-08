import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from collections import Counter
from dotenv import load_dotenv
import pandas as pd
import altair as alt

load_dotenv()
webhook_url = os.getenv("SLACK_WEBHOOK_URL")

st.set_page_config(
    page_title="Threat Trend Insight",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

IGNORE_WORDS = {
    # 文法・一般的単語
    "の", "における", "に関する", "に対する", "および", "または",
    "製品", "複数", "サービス", "システム", "アプリケーション", "ソフトウェア",
    "情報", "管理", "実行", "回避", "方法", "確認", "解決", "対応", "対策",
    "使用", "可能", "公開", "攻撃", "悪用", "影響", "発生", "ユーザー",
    "送信", "受信", "処理", "参照", "生成", "完了", "成功", "失敗", "新規",
    # 形容詞・副詞
    "任意", "不適切", "不足", "不全", "不正", "有効", "無効", "欠如",
    "重要", "重大", "致命的", "危険", "安全", "正常", "異常", "詳細",
    "適切", "不備", "検証", "実装", "設定", "状態", "場所",
    # Stop Words (English)
    "the", "a", "an", "in", "on", "at", "of", "for", "to", "with", "by", "from",
    "and", "or", "is", "are", "was", "were", "be", "has", "have", "it", "this", "that",
    "target", "attack", "remote", "arbitrary", "execution", "denial", "service",
    "improper", "insufficient", "missing", "validation",
    # ドメイン固有
    "脆弱性", "vulnerability", "vulnerabilities", "cve", "jvn",
    "server", "client", "user", "app", "ver", "version", "update",
    "ii", "iii", "iv", "v", "vi",
    "認証", "等", "ベンダ", "ベンダー"
}

PROTECTED_WORDS = {
    "情報漏えい": "InfoLeak",
    "情報漏洩": "InfoLeak",
    "クロスサイトスクリプティング": "XSS",
    "クロスサイト・スクリプティング": "XSS",
    "バッファオーバーフロー": "BufferOverflow",
    "バッファオーバーリード": "BufferOverRead",
    "ディレクトリトラバーサル": "DirectoryTraversal",
    "リモートコード実行": "RCE",
    "サービス運用妨害": "DoS",
    "SQLインジェクション": "SQLi",
    "コマンドインジェクション": "CmdInjection",
    "権限昇格": "PrivEscalation",
    "コード実行": "CodeExec"
}

def normalize_text_for_search(text):
    for jpn, eng in PROTECTED_WORDS.items():
        text = text.replace(jpn, f" {eng} ")
    return text

def fetch_rss_data(limit=None):
    target_url = "https://jvndb.jvn.jp/rss/jvndb.rdf"
    news_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="xml")
            items = soup.find_all("item")
            target_items = items[:limit] if limit else items
            
            for item in target_items:
                news_list.append({
                    "title": item.title.text,
                    "link": item.link.text,
                    "date": item.date.text[:10] if item.date else "---",
                    "description": item.description.text if item.description else ""
                })
        return news_list
    except Exception as e:
        st.error(f"データ取得エラー: {e}")
        return []

def extract_keywords(text):
    text = normalize_text_for_search(text)
    clean_text = re.sub(r'[!-/:-@[-`{-~、。ぁ-ん]', ' ', text)
    words = clean_text.split()
    
    valid_words = []
    for w in words:
        w_lower = w.lower()
        if w_lower in IGNORE_WORDS: continue
        if len(w) < 2: continue
        if w.isdigit(): continue
        valid_words.append(w.capitalize())
    return valid_words

def highlight_title(text, keywords):
    for k in keywords:
        if not k: continue
        pattern = re.compile(re.escape(k), re.IGNORECASE)
        text = pattern.sub(f":orange[{k}]", text)
    return text

def analyze_dynamic_trends(news_data):
    all_words = []
    for item in news_data:
        words = extract_keywords(item['title'])
        all_words.extend(words)
    return Counter(all_words)

def send_daily_report(trend_text, detail_items):
    if not webhook_url: return False

    slack_blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "📅 本日の脆弱性自動分析レポート", "emoji": True}},
        {"type": "section", "text": {"type": "mrkdwn", "text": trend_text}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "🚨 **選別された重要ニュース**"}}
    ]

    for item in detail_items[:7]:
        slack_blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"• <{item['link']}|{item['title']}>\n   date: {item['date']}"}
        })

    try:
        payload = {"blocks": slack_blocks}
        requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        return True
    except:
        return False

st.title("📰 Threat Trend Insight")
st.markdown("ニュースタイトルからキーワードを自動抽出し、トレンド分析と重要ニュースの選定を行います。")

# 検索フィルター
with st.sidebar:
    st.header("⚙️ 検索フィルタ設定")
    
    # 固定監視ワード設定
    default_keywords = "VPN, Remote"
    keywords_input = st.text_input("✅ 固定監視ワード (カンマ区切り)", default_keywords)
    user_watch_keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    st.markdown("---")
    
    # 除外ワード設定
    exclusion_input = st.text_input("⛔ 除外ワード (カンマ区切り)", "Linux, Beta")
    user_exclude_keywords = [k.strip() for k in exclusion_input.split(",") if k.strip()]
    st.caption("※ここに指定した単語を含む記事は、リストと通知から完全に除外されます。")

    st.markdown("---")
    
    # 分析実行ボタン
    if st.button("🔄 分析を開始", type="primary"):
        with st.spinner("最新ニュースを解析中..."):
            raw_data = fetch_rss_data()
            st.session_state["news_data"] = raw_data
            st.success("分析完了")

if "news_data" in st.session_state and st.session_state["news_data"]:
    data = st.session_state["news_data"]
    
    # データ処理
    counter = analyze_dynamic_trends(data)
    top_trends = counter.most_common(10)
    top_10_keywords = [t[0] for t in top_trends]
    
    col_chart, col_list = st.columns([1, 2], gap="large")
    
    # --- 左カラム: トレンド分析 ---
    with col_chart:

        # 1. サマリー
        m1, m2 = st.columns(2)
        m1.metric("分析記事数", f"{len(data)}件")
        m2.metric("ユニーク単語数", f"{len(counter)}語")
        
        st.divider()

        # 2. トレンドグラフ
        st.subheader("📈 トレンド分析 (Top 10)")
        if top_trends:
            df_chart = pd.DataFrame(top_trends, columns=['Keyword', 'Count'])
            
            chart = alt.Chart(df_chart).mark_bar().encode(
                x=alt.X('Keyword', 
                        axis=alt.Axis(labelAngle=-45, labelOverlap=False), 
                        sort='-y', 
                        title=None),
                y=alt.Y('Count', title="出現回数"),
                tooltip=['Keyword', 'Count'],
                color=alt.value('#FFAA00')
            )
            st.altair_chart(chart, use_container_width=True)
            
            trend_text = "*【自動解析トレンド】*\n"
            for word, count in counter.most_common(3):
                trend_text += f"🔥 *{word}* ({count}件)\n"
        else:
            st.info("データ不足のため表示できません")
            trend_text = "トレンドなし"

        st.divider()

        # 3. 頻出単語リスト
        st.subheader("📋 頻出単語リスト")
        st.caption("除外設定や監視ワード候補の検討にご利用ください。")
        
        if counter:
            df_freq = pd.DataFrame(counter.most_common(), columns=['単語', '出現回数'])
            st.dataframe(
                df_freq,
                use_container_width=True,
                height=400,
                hide_index=True
            )

    # --- 右カラム: 重要ニュース選定 ---
    with col_list:
        st.subheader("🚨 選別されたニュース")

        all_filter_options = sorted(list(set(user_watch_keywords + top_10_keywords)))

        # フィルター
        active_filters = st.multiselect(
            "🔍 適用中のフィルター (固定設定 + トレンドTop10)",
            options=all_filter_options,
            default=user_watch_keywords
        )

        st.caption(f"現在のフィルタ条件: {', '.join(active_filters)}")

        filtered_news = []
        for item in data:
            title_search = normalize_text_for_search(item['title'])
            desc_search = normalize_text_for_search(item['description'])
            target_text = (title_search + " " + desc_search).lower()
            
            if any(exc.lower() in target_text for exc in user_exclude_keywords):
                continue
                
            if active_filters:
                if any(k.lower() in target_text for k in active_filters):
                    filtered_news.append(item)
            else:
                pass

        # 検索結果
        if filtered_news:
            st.success(f"該当件数: {len(filtered_news)} 件")
            with st.container(height=900):
                for item in filtered_news:
                    colored_title = highlight_title(item['title'], active_filters)
                    st.markdown(f"**{colored_title}**")
                    st.caption(f"📅 {item['date']} | [Link]({item['link']})")
                    st.divider()
        else:
            st.warning("条件に一致するニュースが見つかりませんでした。フィルターを調整してください。")

    # --- Slack送信エリア ---
    st.markdown("---")
    if st.button(f"📢 分析レポートをSlackへ (新着7件送信 / 全{len(filtered_news)}件)"):
        if send_daily_report(trend_text, filtered_news):
            st.toast("送信完了！", icon="🚀")
            st.balloons()
        else:
            st.error("Slack Webhook URLが設定されていません。")

else:
    st.info("サイドバーの「自動分析を開始」ボタンを押してください。")

# フッターエリア
st.markdown("---")
st.caption("© 2025 Security Engineer Portfolio Demo | Created by eternoi-dev")