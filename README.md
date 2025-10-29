# 🚀 Link Plus 開発環境構築手順

このドキュメントでは、Link Plus のローカル開発環境を構築するための手順を説明します。

---

## 📦 必要環境
- Python 3.12
- Django 5.x
- PostgreSQL 15 以降

---

## 🐘 PostgreSQL のインストール
Link Plus は **PostgreSQL** を使用します。
まだインストールしていない場合は、以下の手順に従ってセットアップしてください。

### Windows
1. [PostgreSQL 公式サイト](https://www.postgresql.org/download/windows/) からインストーラーをダウンロード
2. インストール時に以下を設定
   - ユーザー名: `postgres`
   - パスワード: `postgres`
   - ポート: `5432`
3. インストール後、以下のコマンドでログイン確認
   ```bash
   psql -U postgres
    ```

### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### データベース作成
```bash
psql -U postgres
CREATE DATABASE linkplus;
```
---

## 🛠️ セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/haru186f/link-plus.git
cd link-plus
```

### 2. 仮想環境を作成して有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows の場合はvenv\Scripts\activate
```

### 3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数ファイルを作成
```bash
cp .env.example .env.development    # Windows の場合は copy .env .env.development
```
> 🔑 注意
> .env.example はテンプレートです。
> 各自 .env.development を作成し、SECRET_KEY を自分で生成してください。
> 生成コマンド:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. データベースマイグレーションを実行
```bash
python manage.py migrate --settings=config.settings.development
```

### 6. 開発サーバーを起動
```bash
python manage.py runserver --settings=config.settings.development
```
起動後、以下の URL にアクセスして動作を確認できます。
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧭 開発ルール
| ブランチ名 | 用途 |
|-------------|------|
| `main` | 安定版・本番リリース用 |
| `develop` | 開発の統合ブランチ |
| `feature/xxx` | 新機能追加 |
| `fix/xxx` | バグ修正 |
| `docs/xxx` | ドキュメント修正 |
| `refactor/xxx` | 構造改善 |


## 📝 コミットメッセージ規約
| タイプ | 意味 |
|--------|------|
| `feat` | 新機能追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメント変更 |
| `refactor` | 構造改善（動作に影響なし） |
