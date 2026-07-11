const button = document.getElementById("menu-btn");
const menu = document.getElementById("menu");

button.addEventListener("click", () => {
    menu.classList.toggle("open");
});

document.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdown")) {
        menu.classList.remove("open");
    }
});
