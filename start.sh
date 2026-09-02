#!/usr/bin/env bash
set -e

echo "🧪 =========================================="
echo "   AI Secret Labo. - Local AI Studio (#01)"
echo "   Apple Silicon (Metal GPU) Native Runner"
echo "=========================================="
echo ""

# カレントディレクトリをスクリプトの場所に移動
cd "$(dirname "$0")"

# 1. 仮想環境の確認・作成
if [ ! -d ".venv" ]; then
    echo "📦 Python 仮想環境 (.venv) を作成中..."
    python3 -m venv .venv
    echo "📥 依存パッケージをインストール中 (Metal GPU 有効化)..."
    CMAKE_ARGS="-DGGML_METAL=on" .venv/bin/pip install --upgrade pip
    CMAKE_ARGS="-DGGML_METAL=on" .venv/bin/pip install -r requirements.txt
fi

# 2. アプリケーションの起動
echo "🚀 ローカルAIスタジオを起動しています..."
.venv/bin/python app.py
