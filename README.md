# asl-local-ai (AI Secret Labo. #01)

手元のローカル環境（PC/Mac）で動作する軽量なLLMチャットアプリケーションです。  
外部APIやクラウドサービスへの通信を行わず、手元のマシン内で推論を行います。

---

## 🚀 1. クイックスタート

### 動作環境
* **OS**: macOS (Intel / Apple Silicon) / Windows / Linux
* **Python**: 3.10 以上（.venv 仮想環境で稼働）

### 起動手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/hatrot/asl-local-ai.git
cd asl-local-ai

# 2. 起動スクリプトを実行
./start.sh
```

#### スクリプト（start.sh）の動作
1. Python仮想環境（.venv）を作成し、依存ライブラリをインストール
2. 初回起動時のみ、標準モデル（Qwen 2.5 3B Instruct / 約1.9GB）を models/ ディレクトリに自動ダウンロード
3. LLMモデルをロードしてWebサーバーを起動
4. 自動でブラウザ（http://localhost:8000）を開く

---

## 🎭 2. システムプロンプト

このAIに対するシステムプロンプトは、リポジトリ直下の **`system_prompt.txt`** で管理されています。  
テキストファイルを編集して保存すると、サーバーの再起動なしで次の送信から反映されます。

```text
asl-local-ai/
└── system_prompt.txt
```

---

## 📊 3. リソース消費の目安

| 項目 | 実測値 | 備考 |
| :--- | :--- | :--- |
| 🧠 **物理メモリ消費 (RSS)** | **約 1.29 GB** | 軽量LLMモデル |
| ⚡️ **GPU バッファ** | **約 300 MB** | ユニファイドメモリに展開 |
| ⏱️ **応答開始時間** | **約 1 〜 2 秒** | 入力後に順次ストリーミング出力 |
| 🔋 **待機時CPU負荷** | **0.5% 以下** | アイドル時はほぼ無負荷 |

---

## ⌨️ 4. 操作方法

* **`Enter`**: 改行（日本語IME変換の確定Enterで誤送信されない設計）
* **`Shift + Enter`**: 送信
* 画面右端の送信ボタンをクリックしても送信できます。

---

## 📚 連載・公式マガジン

本プロジェクトは、note連載マガジン **「AI Secret Labo.（AI秘密研究所）」** の連載記事と連動しています。

* **note公式マガジン**: [AI Secret Labo. - note](https://note.com/hatrot/m/m4801473bf6fa)

---

## 📄 License & Author

* **Author**: [hatrot](https://note.com/hatrot)
* **License**: MIT License © 2026 hatrot
