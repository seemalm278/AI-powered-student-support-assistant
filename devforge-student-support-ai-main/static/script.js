const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const suggestionButtons = document.querySelectorAll(".suggestion");

// -------------------------
// Get Current Time
// -------------------------

function currentTime() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

// -------------------------
// Add User Message
// -------------------------

function addUserMessage(text) {

    chatBox.innerHTML += `
    <div class="user-message">

        <div class="avatar">
            <i class="fa-solid fa-user"></i>
        </div>

        <div class="bubble">
            <p>${text}</p>
            <small>${currentTime()}</small>
        </div>

    </div>
    `;

    scrollBottom();
}

// -------------------------
// Add Bot Message
// -------------------------

function addBotMessage(text) {

    chatBox.innerHTML += `
    <div class="bot-message">

        <div class="avatar">
            <i class="fa-solid fa-robot"></i>
        </div>

        <div class="bubble">
            ${text}
            <br><br>
            <small>${currentTime()}</small>
        </div>

    </div>
    `;

    scrollBottom();
}

// -------------------------
// Loading Message
// -------------------------

function showLoading() {

    chatBox.innerHTML += `
    <div id="loading" class="bot-message">

        <div class="avatar">
            <i class="fa-solid fa-robot"></i>
        </div>

        <div class="bubble">

            🤖 Thinking...

        </div>

    </div>
    `;

    scrollBottom();
}

function removeLoading() {

    const loading = document.getElementById("loading");

    if (loading) {
        loading.remove();
    }

}

// -------------------------
// Scroll
// -------------------------

function scrollBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}

// -------------------------
// Send Message
// -------------------------

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    addUserMessage(message);

    messageInput.value = "";

    showLoading();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        removeLoading();

        addBotMessage(data.response);

    }

    catch (error) {

        removeLoading();

        addBotMessage(
            "❌ Unable to connect to the server. Please check whether FastAPI is running."
        );

    }

}

// -------------------------
// Button Click
// -------------------------

sendBtn.addEventListener("click", sendMessage);

// -------------------------
// Press Enter
// -------------------------

messageInput.addEventListener("keypress", function (event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});

// -------------------------
// Suggested Questions
// -------------------------

suggestionButtons.forEach(button => {

    button.addEventListener("click", function () {

        messageInput.value = this.innerText;

        sendMessage();

    });

});

// -------------------------
// Clear Chat
// -------------------------

clearBtn.addEventListener("click", function () {

    chatBox.innerHTML = `
    <div class="bot-message">

        <div class="avatar">
            <i class="fa-solid fa-robot"></i>
        </div>

        <div class="bubble">

            <h3>Chat Cleared ✅</h3>

            <p>

                Hello again! Ask me anything about Python, FastAPI,
                LangChain, LangGraph, GitHub, Render or your DEVFORGE internship.

            </p>

        </div>

    </div>
    `;

});