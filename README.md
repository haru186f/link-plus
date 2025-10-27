# Link Plus 開発環境構築手順

このドキュメントでは、Link Plus のローカル開発環境を構築するための手順を説明します。

---

## 🚀 必要環境
- Python 3.12
- Django 5.x

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
cp .env.example .env    # Windows の場合は copy .env.example .env
```

### 5. データベースマイグレーションを実行
```bash
python manage.py migrate
```

### 6. サーバーを起動
```bash
python manage.py runserver
```

## 🧭 開発ルール
- main：常に最新・安定版（リリースもここから実施）
- feature/xxx：新機能追加用ブランチ  
- fix/xxx：バグ修正用ブランチ  
- docs/xxx：ドキュメント修正用ブランチ  
- refactor/xxx：構造改善用ブランチ


## 📝 コミットメッセージ規約
- feat: 新機能追加
- fix: バグ修正
- docs: ドキュメント変更
- refactor: 構造改善（動作に影響しない変更）

## ⚙️ 実行確認
開発環境の起動後、以下の URL にアクセスして動作を確認できます。  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
