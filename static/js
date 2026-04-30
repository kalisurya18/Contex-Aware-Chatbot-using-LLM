const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Display User Message
    appendMessage('user', message);
    userInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        if (data.error) {
            appendMessage('bot', "Sorry, I'm having trouble connecting to the AI.");
        } else {
            appendMessage('bot', data.response);
        }
    } catch (error) {
        appendMessage('bot', "Error: Server not responding.");
    }
}

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
    div.innerHTML = `<div class="${role === 'user' ? 'user-msg' : 'bot-msg'} p-3 max-w-[80%] shadow-sm">${text}</div>`;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}