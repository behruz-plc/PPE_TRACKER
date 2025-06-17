document.addEventListener("DOMContentLoaded", function () {
    // 🎨 Add a Dark Mode Toggle Button
    let header = document.getElementById("header");
    let toggleBtn = document.createElement("button");
    toggleBtn.innerText = "🌙 Dark Mode";
    toggleBtn.style.marginLeft = "15px";
    toggleBtn.style.cursor = "pointer";
    toggleBtn.onclick = function () {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            toggleBtn.innerText = "☀️ Light Mode";
        } else {
            toggleBtn.innerText = "🌙 Dark Mode";
        }
    };
    header.appendChild(toggleBtn);

    // 🔄 Add a Hover Animation for Admin Panel Rows
    let tableRows = document.querySelectorAll(".table tbody tr");
    tableRows.forEach(row => {
        row.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.02)";
            this.style.transition = "all 0.3s ease-in-out";
        });
        row.addEventListener("mouseleave", function () {
            this.style.transform = "scale(1)";
        });
    });
});
