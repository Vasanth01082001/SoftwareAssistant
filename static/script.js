$(document).ready(function() {
    const chatBody = $("#chat-body");
    const userInput = $("#user_input");
    const sendButton = $("#send-button");

    function appendMessage(role, content) {
        const messageClass = role === "User" ? "user" : "assistant";
        const messageHtml = `
            <div class="message ${messageClass}">
                <p>${content}</p>
            </div>
        `;
        chatBody.append(messageHtml);
        chatBody.scrollTop(chatBody[0].scrollHeight);
    }

    sendButton.on("click", function() {
        const user_input = userInput.val();
        if (user_input) {
            appendMessage("User", user_input);
            $.ajax({
                url: "/chat",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ user_input: user_input }),
                success: function(response) {
                    if (response.status === "success") {
                        appendMessage("Assistant", response.response);
                    } else {
                        alert(response.message);
                    }
                }
            });
            userInput.val('');
        }
    });

    userInput.on("keypress", function(e) {
        if (e.which === 13) {
            sendButton.click();
        }
    });

    // Initial request for employee ID and requested software
    function requestInitialInfo() {
        const employee_id = prompt("Enter Employee ID:");
        const requested_software = prompt("Enter the requested software:");
        if (employee_id && requested_software) {
            $.ajax({
                url: "/get_response",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    employee_id: employee_id,
                    requested_software: requested_software
                }),
                success: function(response) {
                    if (response.status === "success") {
                        appendMessage("Assistant", response.response);
                    } else {
                        alert(response.message);
                    }
                }
            });
        } else {
            alert("Please enter both Employee ID and requested software.");
        }
    }

    requestInitialInfo();
});
