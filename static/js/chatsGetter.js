const chatsList = document.getElementById("chatsList");
const noChatsP = document.createElement("p");
const loader = document.createElement("div")
const noMessages = document.createElement("div")
const messagesContent = document.getElementById("messagesContent")
noMessages.innerText = "No messages";
noMessages.className = "noMessage"
loader.className = "messLoader";
noChatsP.innerText = "No Chats";
let url = "/get_chats";
let globalChatId = null;
let colors = [
    "#a04188",
    "#8427ba",
    "#43678c",
    "#438c83",
    "#438c4f",
    "#858c43",
    "#8c5a43",
    "#8c4343",
]
ulList = []
fetch(url).then(function(response) {
  response.json().then(function(file) {
    for (let i of file["chats"]) {
        const item = document.createElement("li")
        item.addEventListener("click", () => OpenChat(i.id, i.recipient))
        item.innerHTML = `<div class="imageBox">` +
            (i.imagePath ? `<img src="${i.imagePath}"/>` : `<span style="background: ${colors[Math.floor(Math.random() * colors.length)]}">${i.recipient[0]}</span>`) +
            `</div><h3 class="recipientName">${i.recipient}</h3><p>${i.message ? i.message : "no messages yet"}</p>`
        item.chatId = i.id;
        ulList.push(item)
        chatsList.append(item)
    }
    if (!ulList.length) chatsList.append(noChatsP)
  });
});

const chatSearch = document.getElementById("chatSearch");
function Search() {
    for (let i of ulList){
        if (!i.children[1].innerText.toLowerCase().includes(chatSearch.value.toLowerCase())) {
            i.remove()
        } else {
            chatsList.append(i)
        }
    }
}
chatSearch.oninput = Search

const messagesBox = document.getElementById("messagesBox");
const chatsSection = document.getElementById("chatsSection");
const messagesUl = document.getElementById("messagesUl");
const messageInput = document.getElementById("messageInput");
messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        SendMessage();
    }
})
const messagesHeaderName = document.getElementById("messagesHeaderName");
const messageCloseButton = document.getElementById("messageCloseButton");
messageCloseButton.addEventListener("click", CloseChat);
const messageSend = document.getElementById("messageSend")
messageSend.addEventListener("click", SendMessage)
let messagesInterval = null;
const messageList = {}
messagesBox.style.display = "none";
let isFirst = true;
function OpenChat(chatId, chatName) {
    isFirst = true;
    globalChatId = chatId;
    chatsSection.style.gridTemplateAreas = '"header header" "chats messages"';
    messagesBox.style.display = "grid";
    if (messagesInterval !== null) clearInterval(messagesInterval);
    messagesHeaderName.innerText = chatName;
    while( messagesUl.firstChild ){
        messagesUl.removeChild( messagesUl.firstChild );
    }
    messagesUl.append(loader)
    messagesUl.append()
    noMessages.remove()
    messagesInterval = setInterval(() => {
        fetch("/get_messages/" + chatId).then(response => {
            response.json().then(function (file) {
                loader.remove()
                if (!file.error) {
                    if (!file.messages.length) messagesUl.append(noMessages);
                    for (let j = 0; j < file.messages.length; j++) {
                        i = file.messages[j]
                        if (messageList[i.id]) {
                            if (!messagesUl.contains(messageList[i.id])) {
                                messagesUl.append(messageList[i.id])
                            }
                        } else {
                            const item = document.createElement("li")
                            item.messageId = i.id
                            item.className = i.isAuthor ? "authorMessage" : "recipientMessage";
                            item.innerHTML = `<p>${i.content}</p><span>${i.time.split(".")[0]}</span>`
                            messageList[i.id] = item;
                            messagesUl.append(item);
                        }
                    }
                    if (isFirst) {
                        messagesContent.scrollTop = messagesContent.scrollHeight;
                        isFirst = false;
                    }
                }
            })
        })
    }, 1000)
}
function CloseChat() {
    chatsSection.style.gridTemplateAreas = '"header header" "chats chats"';
    messagesBox.style.display = "none";
    clearInterval(messagesInterval)
}
function SendMessage() {
    if (globalChatId !== null) {
        (async () => {
        const rawResponse = await fetch('/add_message', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: messageInput.value,
                chatId: globalChatId
            })
        });
        const content = await rawResponse.json();
        isFirst = true;
        const chat = ulList.filter((item) => item.chatId === globalChatId)[0];
        chat.children[2].innerText = "You: " + messageInput.value;
        messageInput.value = "";
})();
    }
}