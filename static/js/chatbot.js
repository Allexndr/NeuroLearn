// ==========================================
// CHATBOT.JS - AI-Powered Chat Assistant
// ==========================================

class ChatBot {
    constructor() {
        this.toggle = document.getElementById('chatbot-toggle');
        this.window = document.getElementById('chatbot-window');
        this.close = document.getElementById('chatbot-close');
        this.form = document.getElementById('chatbot-form');
        this.input = document.getElementById('chatbot-input');
        this.messages = document.getElementById('chatbot-messages');

        this.init();
    }

    init() {
        this.toggle.addEventListener('click', () => this.openChat());
        this.close.addEventListener('click', () => this.closeChat());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.window.contains(e.target) && !this.toggle.contains(e.target)) {
                this.closeChat();
            }
        });
    }

    openChat() {
        this.window.classList.add('active');
        this.input.focus();
    }

    closeChat() {
        this.window.classList.remove('active');
    }

    async handleSubmit(e) {
        e.preventDefault();

        const userMessage = this.input.value.trim();
        if (!userMessage) return;

        // Add user message to chat
        this.addMessage(userMessage, 'user');
        this.input.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            // Call AI endpoint
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();

            // Remove typing indicator
            this.hideTyping();

            // Add bot response
            if (data.response) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage('Sorry, I couldn\'t process that. Please try again.', 'bot');
            }
        } catch (error) {
            this.hideTyping();
            console.error('Chat error:', error);
            this.addMessage('Oops! Something went wrong. Please try again later. 😅', 'bot');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const strong = document.createElement('strong');
        strong.textContent = sender === 'user' ? 'You' : 'AI Assistant';

        const p = document.createElement('p');
        p.textContent = text;

        messageDiv.appendChild(strong);
        messageDiv.appendChild(p);

        this.messages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        this.messages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTyping() {
        const typing = document.getElementById('typing');
        if (typing) {
            typing.remove();
        }
    }

    scrollToBottom() {
        this.messages.scrollTop = this.messages.scrollHeight;
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Add helpful quick responses
const quickResponses = [
    "How do I generate a course?",
    "What topics can I learn?",
    "Is NeuroLearn free?",
    "How does the AI work?"
];

// You can add these as clickable suggestions in the UI
function addQuickResponses() {
    const chatMessages = document.getElementById('chatbot-messages');
    const quickDiv = document.createElement('div');
    quickDiv.style.cssText = 'display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;';

    quickResponses.forEach(response => {
        const btn = document.createElement('button');
        btn.textContent = response;
        btn.style.cssText = 'padding: 0.5rem 1rem; border: 2px solid var(--accent-purple); border-radius: var(--radius-full); background: white; color: var(--accent-purple); cursor: pointer; font-size: 0.85rem; transition: var(--transition-base);';
        btn.addEventListener('click', () => {
            document.getElementById('chatbot-input').value = response;
            document.getElementById('chatbot-form').dispatchEvent(new Event('submit'));
        });
        quickDiv.appendChild(btn);
    });

    chatMessages.appendChild(quickDiv);
}

// Call after initial bot message loads
setTimeout(() => {
    const botMessages = document.querySelectorAll('.bot-message');
    if (botMessages.length === 1) {
        addQuickResponses();
    }
}, 500);
