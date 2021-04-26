const chatId = document.getElementById("chatId");
const chatIdButton = document.getElementById("chatIdButton");
chatIdButton.addEventListener("click", AddChat);
const errorP = document.getElementById("errorP");
function AddChat() {
    let id = chatId.value;
    if (id) {
        fetch(`/add_chat/${id}`).then(response => {
            response.json().then(function(file) {
                if (file.error) {
                    errorP.className = "error";
                    errorP.innerText = file.error;
                } else if (file.success) {
                    chatId.value = "";
                    errorP.className = "success";
                    errorP.innerText = file.success;
                }
            })
        })
    }
}