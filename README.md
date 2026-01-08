# Security Engineer Portfolio (SecOps & Threat Analysis)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52.2-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Security Engineer Portfolio** は、セキュリティエンジニアの実務（認証管理・完全性確認・脆弱性診断・脅威インテリジェンス）を効率化するために設計された、Python製ツールキットです。
バックエンドのロジック構築から、Streamlitを用いたフロントエンド実装までを一貫して行い、DevSecOpsの実践的なスキルセットを証明するために開発しました。

## 📖 プロジェクト概要 / Overview

### 開発の目的
セキュリティエンジニアとしてのスキルセット（Pythonコーディング、脆弱性診断、情報収集の自動化）を実証するためのポートフォリオです。
実務で発生する「パスワード生成」や「ヘッダー確認」などのタスクを、CLIではなくGUIツールとして統合することで、誰でも扱いやすいセキュリティツールキットを目指しました。

### アーキテクチャ
* **Interface**: Streamlitを用いた、Pythonのみで完結するインタラクティブなWeb UI
* **Core Logic**: 外部ツールに依存せず、Python標準ライブラリとRequestsで実装した診断ロジック
* **Visualization**: Pandasによるデータ加工と、Altairを用いたトレンド情報のグラフ化

## 🛠️ 技術スタック / Tech Stack

| Category | Technology | Version | Description |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10+ | コアロジックおよびスクリプティング |
| **Framework** | Streamlit | 1.52.2 | フロントエンドおよびWebサーバー |
| **Network** | Requests | 2.32.5 | HTTP通信、ヘッダー解析、RSS取得 |
| **Data Analysis** | Pandas | 2.3.3 | データフレーム操作、ログ解析 |
| **Visualization** | Altair | 6.0.0 | 脅威トレンドのグラフ描画 |
| **Scraping** | BeautifulSoup4 | 4.14.3 | HTML/XMLパース、スクレイピング |
| **Security** | Secrets / Hashlib | Std Lib | 暗号学的乱数生成、ハッシュ計算 |
| **Env Mgmt** | python-dotenv | 1.2.1 | 環境変数管理 |

## 📂 ディレクトリ構成 / Directory Structure

```text
SECURITY_TOOLS
├── .streamlit/
│   └── config.toml        # Streamlit UI設定
├── pages/                 # 機能モジュール
│   ├── 1_password_manager.py
│   ├── 2_hash_converter.py
│   ├── 3_header_scanner.py
│   └── 4_threat_insight.py
├── .env                   # 環境変数 (Slack Webhook等)
├── .gitignore             # Git除外設定
├── home.py                # アプリケーションのエントリーポイント
├── requirements.txt       # 依存ライブラリ一覧
└── README.md              # ドキュメント

```

## 🛡️ 収録ツール一覧 / Modules

本アプリケーションは以下の4つのモジュールで構成されています。

### 1. 🔑 Password Manager
`secrets` モジュールを用いた暗号学的に安全なパスワード生成と、正規表現エンジンによる強度判定を行います。
- **Feature**: 任意の長さ・文字種での生成、リアルタイムなポリシー検証。

### 2. #️⃣ Integrity Checker
ファイルやテキストのハッシュ値を計算し、データの完全性を検証します。
- **Feature**: MD5/SHA-256対応。クライアントサイド処理に近い実装で、ファイルの改ざん検知を支援。

### 3. 🌐 Network Recon (Header Scanner)
指定したURLのHTTPレスポンスヘッダーをスキャンし、セキュリティ設定の不備（セキュリティヘッダーの欠落など）を検出します。
- **Feature**: `requests` ライブラリによる診断、サーバー情報の特定、CORS/HSTS設定の確認。

### 4. 📰 Threat Trend Insight
JVN iPedia (脆弱性対策情報データベース) のRSSフィードを解析し、独自のテキストマイニング処理でトレンドを抽出・可視化します。
- **Feature**:
    - 特定キーワード（VPN, Remote等）のフィルタリング
    - Altairによる頻出単語の可視化とランキング表示
    - Slackへの分析レポート自動送信機能（デモモード搭載）

## 🚀 セットアップと起動 / Setup & Usage

### 1. インストール
リポジトリをクローンし、必要なライブラリをインストールします。

```bash
# リポジトリのクローン
git clone https://github.com/eternoi-dev/security_tools.git

# ディレクトリの移動
cd security_tools
```

### 2. 仮想環境の作成とインストール (推奨)
Pythonの仮想環境を作成し、必要なライブラリをインストールします。

```bash
# 仮想環境の作成 (Windows)
python -m venv venv
.\venv\Scripts\activate

# ライブラリの一括インストール
pip install -r requirements.txt
```

### 3. 環境変数の設定 (.env)
Slack通知機能を利用する場合、プロジェクトルートに .env ファイルを作成し、Webhook URLを設定してください。 ※ 設定がない場合、通知機能は自動的に**デモモード（送信不可）**で動作するため、必須ではありません。

```
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 4. アプリケーションの起動
以下のコマンドでローカルサーバーを立ち上げます。

```bash
streamlit run home.py
```

## 🗓️ 開発運用とスケジュール / Development Workflow

### GitHub運用ルール (Git Flow)
本プロジェクトでは、コードの品質を保つために以下のルールで開発しています。

* **main**: 常に正常に動く「完成版」を置く場所。
* **develop**: 開発中の機能を一旦まとめる場所。
* **feature/**: 新しい機能を作ったり直したりする「作業場所」。
    * （例: `feature/add-slack-notify` で作業し、完成したら `develop` へ合流させます）

### 今後の展望 (Roadmap)
現在 `v1.0` (基本機能) をリリース済みです。
次は `v2.0` での設計刷新を経て、最終的にはWeb APIとしての分離を計画しています。

* **Phase 1 (Current): v1.0 リリース** ✅
    * 基本的な4つのセキュリティツールの実装
    * データ可視化とSlack通知機能の統合

* **Phase 2 (Next): v2.0 エンジニアリング強化** 🚧
    * **アーキテクチャ刷新**: スクリプト型からオブジェクト指向（クラス設計）への移行
    * **責務の分離**: ロジック層（計算・通信）とUI層（Streamlit）の完全分離
    * **品質保証**: `pytest` による単体テストの導入と、GitHub Actions（CI）による自動テスト環境の構築
    * **運用ログ**: 動作状況を追跡するためのロギング機能の実装

* **Phase 3 (Future): マイクロサービス化 (FastAPI)**
    * **API分離**: Streamlit内のロジックを切り出し、FastAPI を用いて独立した Web API サーバーを構築
    * **コンテナ化**: Docker を導入し、コマンド一つで環境構築が完了する仕組み（IaC）の実装
    * **API仕様書**: Swagger UI によるドキュメント自動生成と、APIの可視化

## ⚠️ 免責事項 / Disclaimer
本ツールに含まれる **Network Recon** 機能は、自己診断および管理権限を持つ対象への使用を目的としています。
許可のない第三者のサーバーに対してスキャンを行わないでください。
開発者は本ツールの使用によるいかなる損害についても責任を負いません。

---
© 2025 Security Engineer Portfolio Demo | Created by [eternoi-dev](https://github.com/eternoi-dev)