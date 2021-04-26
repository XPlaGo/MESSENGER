const globalUl = document.getElementById("globalUl");
let url = "/get_global";
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
console.log("run")
fetch(url).then(function(response) {
  response.json().then(function(file) {
      console.log(file)
    for (let i of file["users"]) {
        console.log(i);
        const item = document.createElement("li")
        item.innerHTML = `<div class="imageBox">` +
            (i.imagePath ? `<img src="${i.imagePath}"/>` : `<span style="background: ${colors[Math.floor(Math.random() * colors.length)]}">${i.name[0]}</span>`) +
            `</div><h3 class="recipientName">${i.name}</h3><p>ID: ${i.id}</p>${!i.isRecipient ? `<button>Add Chat</button>` : ""}`
        if (item.children[3]) {
            item.children[3].addEventListener("click", () => AddChatGlobal(i.id))
        }
        ulList.push(item)
        globalUl.append(item)
    }
  });
});
const globalSearch = document.getElementById("globalSearch");
function Search() {
    console.log(globalSearch.value);
    for (let i of ulList){
        if (!i.children[1].innerText.toLowerCase().includes(globalSearch.value.toLowerCase())) {
            i.remove()
        } else {
            globalUl.append(i)
        }
    }
}
globalSearch.oninput = Search
function AddChatGlobal(recipientId) {
    console.log(recipientId)
    if (recipientId) {
        fetch(`/add_chat/${recipientId}`, {
            method: "POST"
        }).then(
            location.reload()
        )
    }
}