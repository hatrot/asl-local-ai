const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages-container');

let conversationHistory = [];

// テキストエリアの自動伸縮
chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
});

// Shift+Enter のみ送信。Enter単体は改行（日本語IME変換の誤送信を防止）
chatInput.addEventListener('keydown', (e) => {
  if (e.isComposing) return; // IME変換中は無視

  if (e.key === 'Enter' && e.shiftKey) {
    e.preventDefault();
    chatForm.dispatchEvent(new Event('submit'));
  }
});

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = chatInput.value.trim();
  if (!text) return;

  // 入力欄をクリア
  chatInput.value = '';
  chatInput.style.height = 'auto';
  chatInput.disabled = true;
  sendBtn.disabled = true;

  // ユーザーメッセージを追加
  appendMessage('user', text);
  conversationHistory.push({ role: 'user', content: text });

  // AIメッセージ枠を作成
  const aiMessageElement = appendMessage('ai', '');

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: conversationHistory })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let aiFullText = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.replace('data: ', '').trim();
          if (dataStr === '[DONE]') break;
          try {
            const data = JSON.parse(dataStr);
            if (data.content) {
              aiFullText += data.content;
              aiMessageElement.textContent = aiFullText;
              messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
          } catch (err) {
            // parse error ignore
          }
        }
      }
    }

    conversationHistory.push({ role: 'assistant', content: aiFullText });

  } catch (err) {
    aiMessageElement.textContent = '❌ エラーが発生しました: ' + err.message;
  } finally {
    chatInput.disabled = false;
    sendBtn.disabled = false;
    chatInput.focus();
  }
});

function appendMessage(role, text) {
  const welcome = document.querySelector('.welcome-message');
  if (welcome) welcome.remove();

  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  const avatar = document.createElement('div');
  avatar.className = `avatar ${role}`;
  avatar.textContent = role === 'user' ? 'U' : 'AI';

  const content = document.createElement('div');
  content.className = 'message-content';
  content.textContent = text;

  if (role === 'ai') {
    row.appendChild(avatar);
    row.appendChild(content);
  } else {
    row.appendChild(content);
    row.appendChild(avatar);
  }

  messagesContainer.appendChild(row);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  return content;
}
