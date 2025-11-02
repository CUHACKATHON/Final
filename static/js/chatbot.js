// Anonymous Chatbot Interface
// Session management using localStorage

(function() {
    let sessionId = localStorage.getItem('chatSessionId');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    const crisisAlert = document.getElementById('crisis-alert');

    // Initialize session if not exists
    if (!sessionId) {
        sessionId = null; // Will be created on first message
    }

    // Add message to chat
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Format text with line breaks
        const formattedText = text.split('\n').map(line => {
            if (line.trim().startsWith('•') || line.trim().match(/^\d+\./)) {
                return `<strong>${line}</strong>`;
            }
            return line;
        }).join('<br>');
        
        bubble.innerHTML = formattedText;
        messageDiv.appendChild(bubble);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show/hide typing indicator
    function showTyping() {
        typingIndicator.classList.add('active');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTyping() {
        typingIndicator.classList.remove('active');
    }

    // Send message to server
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Disable input
        chatInput.disabled = true;
        sendButton.disabled = true;

        // Add user message to chat
        addMessage(message, true);
        chatInput.value = '';

        // Show typing indicator
        showTyping();

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Save session ID
                if (data.session_id) {
                    sessionId = data.session_id;
                    localStorage.setItem('chatSessionId', sessionId);
                }

                // Hide typing indicator
                hideTyping();

                // Add bot response
                addMessage(data.response, false);

                // Handle crisis detection
                if (data.crisis_detected) {
                    crisisAlert.style.display = 'block';
                }

                // Handle suggested actions
                if (data.suggested_action === 'book_appointment' || data.suggested_action === 'suggest_counseling') {
                    setTimeout(() => {
                        const appointmentPrompt = document.createElement('div');
                        appointmentPrompt.className = 'message bot';
                        appointmentPrompt.innerHTML = `
                            <div class="message-bubble">
                                Would you like to <a href="/appointments/" style="color: #3498db; text-decoration: underline;">book an appointment</a> with a counselor?
                            </div>
                        `;
                        chatMessages.appendChild(appointmentPrompt);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    }, 1000);
                }
            } else {
                hideTyping();
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        } catch (error) {
            hideTyping();
            addMessage('Sorry, there was a connection error. Please check your internet connection and try again.', false);
            console.error('Error:', error);
        }

        // Re-enable input
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);

    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Focus input on load
    chatInput.focus();
})();

