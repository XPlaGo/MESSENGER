imageBox = document.getElementById("imageBox");
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
infoBlock = document.getElementById("infoBlock");
url = "/get_current_user";
fetch(url).then(function(response) {
    response.json().then(function(file) {
        imageBox.innerHTML = `<span style="background: ${colors[Math.floor(Math.random() * colors.length)]}">${file["Name"][0]}</span>`
        for (let i in file) {
            const h = document.createElement("h3")
            h.innerText = i + ":";
            const p = document.createElement("p")
            p.innerText = file[i];
            infoBlock.append(h);
            infoBlock.append(p);
    }
    });
});
