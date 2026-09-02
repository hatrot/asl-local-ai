import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

app = FastAPI(title="AI Secret Labo. - Local AI Studio")

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
MODEL_FILENAME = "qwen2.5-3b-instruct-q4_k_m.gguf"
MODEL_PATH = MODELS_DIR / MODEL_FILENAME
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"

def get_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    return "あなたは親切なAIアシスタントです。"

print(f"📦 モデルの確認中: {MODEL_PATH}")
if not MODEL_PATH.exists():
    print("📥 初回モデルの自動ダウンロード中 (Qwen2.5 3B / 約1.9GB)...")
    hf_hub_download(
        repo_id="Qwen/Qwen2.5-3B-Instruct-GGUF",
        filename=MODEL_FILENAME,
        local_dir=str(MODELS_DIR)
    )

print("🚀 Metal GPU (Apple Silicon / CUDA) へのモデルロード中...")
llm = Llama(
    model_path=str(MODEL_PATH),
    n_gpu_layers=-1,  # GPUに全層オフロード (Metal / CUDA自動判別)
    n_ctx=2048,
    verbose=False
)
print("✅ モデル準備完了！推論エンジンがスタンバイしました。")

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    messages: list[dict]

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    system_prompt = get_system_prompt()
    
    # Qwen2.5 の ChatML テンプレートに変換
    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
    for msg in req.messages:
        role = msg.get("role", "user")
        if role == "system":
            continue
        content = msg.get("content", "")
        prompt += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    def event_stream():
        stream = llm(
            prompt,
            max_tokens=1024,
            stop=["<|im_end|>"],
            stream=True
        )
        for chunk in stream:
            delta = chunk["choices"][0]["text"]
            if delta:
                import json
                yield f"data: {json.dumps({'content': delta}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/")
async def index_page():
    return FileResponse(STATIC_DIR / "index.html")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    import uvicorn
    threading.Thread(target=open_browser, daemon=True).start()
    print("\n🌐 Web UI を起動しました: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
