document.getElementById("toggleTheme").addEventListener("click", function () {
    document.body.classList.toggle("dark-theme");
});

// 增加暗色模式樣式
const style = document.createElement("style");
style.innerHTML = `
.dark-theme {
    background-color: #333;
    color: #fff;
}
.dark-theme .about {
    background-color: #555;
}
.dark-theme button {
    background-color: #888;
}
.dark-theme button:hover {
    background-color: #666;
}`;
document.head.appendChild(style);