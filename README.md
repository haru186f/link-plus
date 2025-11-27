# 🚀 Link Plus 開発環境構築 & 開発手順

このドキュメントでは、**Link Plus** のローカル開発環境の構築方法と、<br>
チームでの開発フロー（ブランチ運用・コミット・PR作成）について説明します。

---

## 📦 必要環境
- Python 3.12
- Django 5.x
- PostgreSQL 15 以降

---

## 🐘 PostgreSQL のインストール
Link Plus は **PostgreSQL** を使用します。<br>
未インストールの場合は、以下の手順でセットアップしてください。

### Windows
1. [PostgreSQL 公式サイト](https://www.postgresql.org/download/windows/) からインストーラーをダウンロード
2. インストール時の設定
   - ユーザー名: `postgres`
   - パスワード: `postgres`
   - ポート: `5432`
3. インストール後、以下のコマンドでログインし、データベースを作成
   ```bash
   psql -U postgres
   CREATE DATABASE linkplus;
    ```

### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo -u postgres psql
CREATE DATABASE linkplus;
```

---

# 🛠️ セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/haru186f/link-plus.git
cd link-plus
```

### 2. 仮想環境を作成して有効化
```bash
python -m venv venv
source venv/bin/activate
# Windows の場合： venv\Scripts\activate
```

### 3. パッケージをインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数ファイルを作成
```bash
cp .env.example .env.development
# Windows の場合： copy .env.example .env.development
```
> 🔑 注意<br>
> `.env.example`はテンプレートです。<br>
> 各自`.env.development`を作成し、`SECRET_KEY`を生成してください。<br>
> 生成コマンド:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. データベースマイグレーションを実行
```bash
python manage.py migrate
```

### 6. 初期データを投入（カスタムコマンド一括実行）
```bash
python manage.py run_all_custom_commands
```

### 7. 開発サーバーを起動
```bash
python manage.py runserver
```
起動後、以下のURLにアクセスして動作を確認できます。<br>
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

# 💻 チーム開発の進め方

### 1. 最新の`main`を取得
作業を始める前に、常に最新の main ブランチを取得してください。

```bash
git switch main
git pull origin main
```

> 💡 注意<br>
> 他の開発者の変更を取り込まないまま作業を続けると、**コンフリクト**の原因になります。<br>
> 作業中でも、**定期的に `main` を pull して最新の状態を保つ**ようにしましょう。

---

### 2. 新しいブランチを作成
新しい作業を始めるときは、必ず`main`から新しいブランチを作成してください。<br>
ブランチ名は「何をするブランチか」が明確に分かるように命名しましょう。
```bash
git switch -c feat/your-branch-name
```
> 🏷️ ブランチ命名規則
> | 種類 | 例 |
> |-------------|------|
> | 新機能 | `feat/add-login-page` |
> | バグ修正 | `fix/user-login-error` |
> | 構造改善 | `refactor/update-model-structure` |
> | ドキュメント修正 | `docs/update-readme` |

---

### 3. 開発・コミット
作業中の変更は、**小さく・こまめにコミット**することを意識してください。<br>
「1コミット＝1目的」を基本とし、複数の修正をまとめすぎないようにしましょう。

```bash
git add --all
git commit -m "feat: ログイン画面を追加"
```
> 💬 コミットメッセージの書き方
> | タイプ | 説明 | 例 |
> |-------------|------|------|
> | feat | 新しい機能を追加 | `feat: ユーザープロフィール編集機能を追加` |
> | fix | 不具合を修正 | `fix: ログイン時に500エラーが発生する問題を修正` |
> | refactor | 構造を改善（動作変更なし） | `refactor: models.pyの構造を整理` |
> | docs | ドキュメントを変更 | `docs: READMEにセットアップ手順を追記` |

---

### 4. リモートへプッシュ
作業が完了したら、ブランチをリモートへプッシュします。

```bash
git push origin feat/your-branch-name
```

> 💡 補足<br>
> 初回のみブランチ名を明示します。<br>
> 2回目以降は git push のみでOKです。

---

### 5. Pull request (PR) を作成
GitHub上で、`feat/your-branch-name`→`main`への**Pull Request**を作成します。<br>
PRタイトルはコミットメッセージと同様の形式で記述してください。
> 💡 補足<br>
> PR本文には「変更内容」「目的」「確認手順」などを簡潔に記載するとレビューがスムーズになります。<br>
> 作業途中の場合は `[WIP]`（Work In Progress）をタイトルに付けてください。
