"""
Web-based Chatbot for Holdings and Trades Data Analysis
Run with: python web_chatbot.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
from chatbot import DataChatbot

app = Flask(__name__)
chatbot = DataChatbot()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Financial Analyst</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <!-- Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-primary: #111827;
            --text-secondary: #6b7280;
            --bot-bubble-bg: #f3f4f6;
            --user-bubble-bg: #4f46e5;
            --user-text-color: #ffffff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Main Chat Container */
        .chat-container {
            width: 100%;
            max-width: 900px;
            height: 90vh;
            background-color: var(--card-bg);
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }

        /* Header */
        .chat-header {
            padding: 20px 30px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            z-index: 10;
        }

        .header-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .bot-avatar-large {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #4f46e5, #818cf8);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }

        .header-text h1 {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .header-text p {
            font-size: 0.875rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
        }

        /* Chat Area */
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 30px;
            scroll-behavior: smooth;
        }

        .message-wrapper {
            display: flex;
            margin-bottom: 24px;
            opacity: 0;
            animation: fadeIn 0.3s ease forwards;
        }

        @keyframes fadeIn {
            to { opacity: 1; transform: translateY(0); }
        }

        .message-wrapper.bot {
            justify-content: flex-start;
        }

        .message-wrapper.user {
            justify-content: flex-end;
        }

        .bot-avatar-small {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #4f46e5, #818cf8);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 14px;
            margin-right: 12px;
            flex-shrink: 0;
        }

        .message-content {
            max-width: 70%;
            padding: 16px 20px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.6;
            position: relative;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        .message-wrapper.bot .message-content {
            background-color: var(--bot-bubble-bg);
            color: var(--text-primary);
            border-top-left-radius: 4px;
        }

        .message-wrapper.user .message-content {
            background-color: var(--user-bubble-bg);
            color: var(--user-text-color);
            border-top-right-radius: 4px;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }

        .message-time {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 6px;
            margin-left: 5px;
        }

        .message-wrapper.user .message-time {
            text-align: right;
            margin-right: 5px;
        }

        /* Suggestions */
        .suggestions-container {
            padding: 10px 30px 20px;
            display: flex;
            gap: 10px;
            overflow-x: auto;
            scrollbar-width: none; /* Firefox */
        }
        
        .suggestions-container::-webkit-scrollbar {
            display: none; /* Chrome, Safari, Opera */
        }

        .suggestion-chip {
            padding: 8px 16px;
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            color: var(--text-primary);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }

        .suggestion-chip:hover {
            background-color: #e0e7ff;
            color: var(--primary-color);
            border-color: #c7d2fe;
            transform: translateY(-1px);
        }

        /* Input Area */
        .input-area {
            padding: 20px 30px 30px;
            background-color: white;
            border-top: 1px solid #f3f4f6;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        #user-input {
            width: 100%;
            padding: 16px 60px 16px 24px;
            background-color: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 16px;
            font-size: 1rem;
            font-family: inherit;
            outline: none;
            transition: all 0.2s;
        }

        #user-input:focus {
            border-color: var(--primary-color);
            background-color: white;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        .send-btn {
            position: absolute;
            right: 12px;
            width: 44px;
            height: 44px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .send-btn:hover {
            background-color: var(--primary-hover);
            transform: scale(1.05);
        }
        
        .send-btn:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
            transform: none;
        }

        /* Typing Indicator */
        .typing-indicator {
            display: none;
            padding: 15px 20px;
            background-color: var(--bot-bubble-bg);
            border-radius: 18px;
            border-top-left-radius: 4px;
            width: fit-content;
            margin-bottom: 20px;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .dot {
            width: 8px;
            height: 8px;
            background-color: #9ca3af;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }

        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* Responsive */
        @media (max-width: 640px) {
            .chat-container {
                height: 100vh;
                max-width: 100%;
                border-radius: 0;
            }
            
            .message-content {
                max-width: 85%;
            }
        }
        
        /* Markdown-like Styles within messages */
        .message-content strong {
            font-weight: 600;
        }
        
        .message-content ul, .message-content ol {
            margin-left: 20px;
            margin-top: 8px;
            margin-bottom: 8px;
        }
        
        .message-content li {
            margin-bottom: 4px;
        }
        
        .message-content p {
            margin-bottom: 8px;
        }
        
        .message-content p:last-child {
            margin-bottom: 0;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <!-- Header -->
        <div class="chat-header">
            <div class="header-info">
                <div class="bot-avatar-large">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="header-text">
                    <h1>FinBot Analyst</h1>
                    <p><span class="status-dot"></span> Online & Ready</p>
                </div>
            </div>
        </div>

        <!-- Chat Messages -->
        <div class="chat-messages" id="chat-messages">
            <!-- Parameters: Content, Time, IsUser -->
            <div class="message-wrapper bot">
                <div class="bot-avatar-small">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Hello! I'm your AI Financial Analyst. I can help you analyze your <strong>Holdings</strong> and <strong>Trades</strong> data.</p>
                    <p>Try one of the suggestions below or type your own question!</p>
                </div>
            </div>
        </div>

        <!-- Typing Indicator -->
        <div class="typing-indicator" id="typing-indicator">
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>

        <!-- Suggestions -->
        <div class="suggestions-container">
            <button class="suggestion-chip" onclick="askQuestion('Total number of holdings')">📊 Total Holdings</button>
            <button class="suggestion-chip" onclick="askQuestion('Which funds performed better?')">📈 Best Funds</button>
            <button class="suggestion-chip" onclick="askQuestion('YTD P&L for Ytum')">💰 YTD P&L</button>
            <button class="suggestion-chip" onclick="askQuestion('How many buy trades?')">🛒 Buy Trades</button>
            <button class="suggestion-chip" onclick="askQuestion('List all funds')">📋 List Funds</button>
        </div>

        <!-- Input Area -->
        <div class="input-area">
            <div class="input-wrapper">
                <input type="text" id="user-input" placeholder="Type your question here..." autocomplete="off">
                <button class="send-btn" id="send-btn" onclick="sendMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const typingIndicator = document.getElementById('typing-indicator');

        function formatTime(date) {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        function createMessageElement(content, isUser) {
            const wrapper = document.createElement('div');
            wrapper.className = `message-wrapper ${isUser ? 'user' : 'bot'}`;
            
            let avatarHtml = '';
            if (!isUser) {
                avatarHtml = `
                    <div class="bot-avatar-small">
                        <i class="fas fa-robot"></i>
                    </div>
                `;
            }
            
            // Convert newlines to <br> and handle rudimentary formatting if needed
            // Ideally, we'd use a Markdown parser, but for now strict text replacement:
            const formattedContent = content
                .replace(/\\n/g, '<br>')
                .replace(/•/g, '<br>•'); 

            wrapper.innerHTML = `
                ${avatarHtml}
                <div>
                    <div class="message-content">${formattedContent}</div>
                    <div class="message-time">${formatTime(new Date())}</div>
                </div>
            `;
            
            return wrapper;
        }

        function addMessage(content, isUser) {
            const messageEl = createMessageElement(content, isUser);
            
            // Add before typing indicator if it exists/is visible, or just append
             // Actually, the typing indicator is outside the chat-messages div in design, 
             // but let's just append to chatMessages.
            chatMessages.appendChild(messageEl);
            scrollToBottom();
        }

        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTyping() {
            // In this design, let's just append the typing indicator to the message list temporarily
            // Or better, just toggle visibility of a fixed indicator?
            // Let's create a temporary typing message inside the list for better flow
            const wrapper = document.createElement('div');
            wrapper.className = 'message-wrapper bot typing-message';
            wrapper.id = 'temp-typing';
            wrapper.innerHTML = `
                <div class="bot-avatar-small">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content" style="padding: 12px 18px;">
                    <div class="typing-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            `;
            chatMessages.appendChild(wrapper);
            scrollToBottom();
        }

        function hideTyping() {
            const typingMsg = document.getElementById('temp-typing');
            if (typingMsg) {
                typingMsg.remove();
            }
        }

        function askQuestion(question) {
            userInput.value = question;
            sendMessage();
        }

        async function sendMessage() {
            const question = userInput.value.trim();
            if (!question) return;

            // Disable input
            userInput.disabled = true;
            sendBtn.disabled = true;

            // Add user message
            addMessage(question, true);
            userInput.value = '';

            // Show typing
            showTyping();

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                
                // Simulate a slight delay for realism if response is instant
                setTimeout(() => {
                    hideTyping();
                    addMessage(data.answer, false);
                    
                    // Re-enable input
                    userInput.disabled = false;
                    sendBtn.disabled = false;
                    userInput.focus();
                }, 500);

            } catch (error) {
                hideTyping();
                addMessage('Sorry, there was an error processing your request.', false);
                userInput.disabled = false;
                sendBtn.disabled = false;
            }
        }

        // Event Listeners
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Initial Focus
        userInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    answer = chatbot.process_question(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Holdings & Trades Web Chatbot")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
