# ----------------------
# ベースイメージ
# ----------------------
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /sagyou

# 必要パッケージインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存関係コピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコピー
COPY . .

# 環境変数読み込み（Docker Compose で .env をマウント推奨）
ENV PYTHONUNBUFFERED=1

